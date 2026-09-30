"""Drive the program's own interview loop over the written applicants, one arm at a time.

    python3 experiment/run.py jev1       [ids...]   # one Jev call per judgement
    python3 experiment/run.py jev        [ids...]   # the same, samples=3: what the extra two cost
    python3 experiment/run.py baseline   [ids...]   # the same loop, a generative model as the judge

Nothing in the loop is reimplemented here. The program is imported and `next_turn`,
`question_payload`, `finish` and `record_outcome` are called the way `do_answer` calls them;
the only thing an arm changes is `app.ask_jev`. Every judge call is metered into
experiment/logs/<arm>.jsonl, and every record the program writes lands in results/<arm>/.

PROGRAM names the checkout of the program (default: ../lab-jev-interview, i.e. a sibling
directory). `core.py` reads interface.json from the working directory, so this chdirs into it.
"""
import json, os, pathlib, re, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
PROGRAM = pathlib.Path(os.environ.get("PROGRAM", REPO.parent / "lab-jev-interview")).resolve()
ARM = sys.argv[1]                # jev | jev1 | baseline, optionally suffixed: jev-rep2 is a repeat run
JUDGE = ARM.split("-")[0]
ONLY = set(sys.argv[2:])
BASELINE_MODEL = os.environ.get("BASELINE_MODEL", "haiku")

# The program reads its environment at import; these are set first so they win.
os.environ["DATA_REPO"] = ""             # never commit an experiment record anywhere
os.environ["GITHUB_TOKEN"] = ""
os.environ["NOTIFY_URL"] = ""
os.environ["RESULTS"] = str(REPO / "results" / ARM)
os.environ["CANDIDATES"] = str(REPO / "candidates")
os.environ["PLAN"] = str(REPO / "plans" / "interview-ja.json")
os.chdir(PROGRAM)
sys.path.insert(0, str(PROGRAM))
import app  # noqa: E402

SPEC = json.loads((HERE / "spec.json").read_text())
ANSWERS = json.loads((HERE / "candidates.json").read_text())["answers"]
LOG = HERE / "logs" / f"{ARM}.jsonl"
LOG.parent.mkdir(exist_ok=True)

# ── metering: every judge call, whichever judge ──────────────────────────
calls: list[dict] = []          # this interview's calls, flushed into the log per interview

def kind_of(questions: dict) -> str:
    if app.FIT in questions:
        return "score"
    if "widget" in questions:
        return "widget"
    return "turn"

REAL_ASK_JEV = app.ask_jev
if not hasattr(app, "JEV_USAGE"):
    raise SystemExit(f"{PROGRAM}/app.py has no JEV_USAGE: it predates the usage hook."
                     " Point PROGRAM at a checkout that has it.")

def metered_jev(state, questions):
    body = json.dumps({"state": state, "model": app.JEV_MODEL, "questions": questions}).encode()
    before = len(app.JEV_USAGE)
    started = time.time()
    answer = REAL_ASK_JEV(state, questions)
    elapsed = time.time() - started
    usage = app.JEV_USAGE[before] if len(app.JEV_USAGE) > before else {}
    calls.append({"kind": kind_of(questions), "ok": answer is not None, "seconds": round(elapsed, 3),
                  "bytes": len(body), "input_tokens": usage.get("input_tokens"),
                  "output_tokens": usage.get("output_tokens"), "options": len(questions.get("next", {}).get("criteria", {}))})
    return answer

# ── the baseline judge: a generative model given the identical request ───
SYSTEM = ("You are the judge inside an adaptive interview program. You receive one JSON request "
          "with `state` (the job brief as `job_context`, and `answers_so_far`) and `questions`. "
          "Answer every question in `questions`, keyed by its name, using only the criteria "
          "given. For type `choice`: pick one key of `criteria` and give a probability for every "
          "key (they sum to 1). For type `noul`: give the probability that `criteria.true` holds "
          "rather than `criteria.false`. For type `score`: `criteria` is an ordered list of "
          "levels, worst first; give a probability for each level index as a string key "
          "(\"0\", \"1\", ...), summing to 1. Judge from the answers only. Output format: one JSON "
          "object whose keys are the question names. For a `choice` question the value is "
          "{\"choice\": <key>, \"probabilities\": {<key>: <p>, ...}}; for a `noul` question "
          "{\"noul\": <p>}; for a `score` question {\"probabilities\": {\"0\": <p>, \"1\": <p>, ...}}. "
          "No prose, no code fence.")

def parse_json(text: str, wanted: dict) -> dict | None:
    """The model's reply as JSON with every question answered, or None. The CLI's structured
    output mode (`--json-schema`) was tried first and failed every scoring request: with
    eleven required objects Haiku never satisfied the schema in five attempts."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", (text or "").strip())
    try:
        parsed = json.loads(text)
    except ValueError:
        return None
    return parsed if isinstance(parsed, dict) and set(parsed) >= set(wanted) else None

def claude_once(prompt: str, wanted: dict) -> tuple[dict | None, dict]:
    """One `claude -p` call, as bare as the CLI allows: no tools, no MCP, no settings."""
    started = time.time()
    # Extended thinking is off unless BASELINE_THINKING says otherwise: with it on, one
    # judgement took 47-103 s and 5,000-9,000 output tokens on the pilot.
    env = os.environ | {"MAX_THINKING_TOKENS": os.environ.get("BASELINE_THINKING", "0")}
    proc = subprocess.run(["claude", "-p", prompt, "--model", BASELINE_MODEL, "--output-format", "json",
                           "--max-turns", "1", "--tools", "", "--system-prompt", SYSTEM,
                           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                           "--setting-sources", "", "--disable-slash-commands"],
                          capture_output=True, text=True, timeout=600, cwd=str(HERE), env=env)
    wall = time.time() - started
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        return None, {"seconds": round(wall, 3), "error": (proc.stderr or proc.stdout)[-300:]}
    answered = parse_json(out.get("result"), wanted)
    usage = out.get("usage", {})
    meter = {"seconds": round(wall, 3), "api_seconds": round(out.get("duration_api_ms", 0) / 1000, 3),
             "input_tokens": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
             + usage.get("cache_read_input_tokens", 0),
             "cache_read_tokens": usage.get("cache_read_input_tokens", 0),
             "output_tokens": usage.get("output_tokens", 0),
             "thinking_tokens": (usage.get("output_tokens_details") or {}).get("thinking_tokens", 0),
             "cost_usd": out.get("total_cost_usd"),
             "unparsed": None if answered is not None else (out.get("result") or "")[:200]}
    return answered, meter

def baseline_judge(state, questions):
    request = json.dumps({"state": state, "questions": questions}, ensure_ascii=False)
    meter, answered = {}, None
    for attempt in range(3):
        answered, meter = claude_once(request, questions)
        if answered is not None:
            break
        time.sleep(2 * 2**attempt)
    row = {"kind": kind_of(questions), "ok": answered is not None, "bytes": len(request.encode()),
           "attempts": attempt + 1, "options": len(questions.get("next", {}).get("criteria", {}))} | meter
    calls.append(row)
    if answered is None:
        return None
    # The same shape Jev returns: `score` is the probability-weighted level, `confidence` the
    # mass on the winner. Both are arithmetic on the distribution the model gave.
    answer = {}
    for name, q in questions.items():
        got = answered.get(name) or {}
        if q["type"] == "choice":
            odds = got.get("probabilities") or {}
            choice = got.get("choice") if got.get("choice") in q["criteria"] else (max(odds, key=odds.get) if odds else None)
            if choice is None:
                row["invalid"] = row.get("invalid", 0) + 1
                continue
            answer[name] = {"choice": choice, "probabilities": odds, "confidence": odds.get(choice, 1.0)}
        elif q["type"] == "noul":
            answer[name] = {"noul": float(got.get("noul", 0.0))}
        else:
            odds = {k: float(v) for k, v in (got.get("probabilities") or {}).items()}
            total = sum(odds.values()) or 1.0
            odds = {k: v / total for k, v in odds.items()}
            answer[name] = {"score": sum(int(k) * v for k, v in odds.items()),
                            "confidence": max(odds.values()) if odds else 0.0, "probabilities": odds}
    return answer

# ── one interview, exactly as the server would run it ────────────────────
def interview(row: dict) -> dict:
    calls.clear()
    answers = ANSWERS[row["id"]]
    state = app.new_state(row["id"])
    started = time.time()
    question_id = app.FIRST_QUESTION
    app.question_payload(state, question_id)          # the first question, as /start serves it
    while question_id:
        state["answers"][question_id] = answers[question_id]
        state["asked"].append(question_id)
        question_id, _ = app.next_turn(state)          # asks the judge; None means it finished
        state["pending"] = question_id
    wall = time.time() - started
    latest = max((REPO / "results" / ARM).glob(f"*-{row['id']}.json"), key=lambda p: p.stat().st_mtime)
    record = json.loads(latest.read_text())
    if row["label"] in ("hire", "reject"):             # a person's decision: the label, filed on the record
        app.record_outcome(latest.name, "hired" if row["label"] == "hire" else "not_hired")
    summary = {"id": row["id"], "arm": ARM, "lang": row["lang"], "type": row["type"], "label": row["label"],
               "record": latest.name, "turns": len(record["answers"]), "total": record["total"],
               "fit": (record.get("fit") or {}).get("score"), "scored": record["scored"],
               "dimensions": {k: v["score"] for k, v in record["dimensions"].items()},
               "order": [r["qid"] for r in record["answers"]],
               "flags": [f["kind"] for f in record["flags"] if f["kind"] != "human_review"],
               "wall_seconds": round(wall, 2),
               "calls": len(calls), "failed_calls": sum(1 for c in calls if not c["ok"]),
               "judge_seconds": round(sum(c.get("api_seconds", c["seconds"]) for c in calls), 2),
               "process_seconds": round(sum(c["seconds"] for c in calls), 2),
               "bytes": sum(c["bytes"] for c in calls),
               "input_tokens": sum(c.get("input_tokens") or 0 for c in calls),
               "output_tokens": sum(c.get("output_tokens") or 0 for c in calls),
               # A judge that reports no price is not a judge that costs nothing, so this
               # stays None rather than collapsing to 0. Jev returns no price per call.
               "cost_usd": (round(sum(priced), 4) if (priced := [c["cost_usd"] for c in calls
                            if c.get("cost_usd") is not None]) else None),
               "per_call": list(calls)}
    with LOG.open("a") as log:
        log.write(json.dumps(summary, ensure_ascii=False) + "\n")
    return summary

def main() -> None:
    if JUDGE == "baseline":
        app.ask_jev = baseline_judge
        app.judge_version = lambda: {"model": f"claude-{BASELINE_MODEL}", "via": "claude -p"}
    else:
        app.ask_jev = metered_jev
    done = {json.loads(line)["id"] for line in LOG.read_text().splitlines()} if LOG.exists() else set()
    shard, shards = (int(x) for x in os.environ.get("SHARD", "0/1").split("/"))   # k/n: every nth
    lang = None
    for at, cid in enumerate(SPEC["order"]):
        row = next(r for r in SPEC["candidates"] if r["id"] == cid)
        if (ONLY and cid not in ONLY) or (not ONLY and cid in done) or at % shards != shard:
            continue
        if row["lang"] != lang:                       # one plan per language; boot the right one
            lang = row["lang"]
            app.PLAN_PATH = pathlib.Path(REPO / "plans" / f"interview-{lang}.json")
            app.boot()
            # One call per judgement: jev1 to compare like for like, and the baseline because
            # a generative judge is not normally asked the same thing three times over.
            if JUDGE in ("jev1", "baseline"):
                app.POLICY["samples"] = 1
        summary = interview(row)
        print(f"{cid} {lang} {row['label']:10} turns={summary['turns']:2} total={summary['total']}"
              f" fit={summary['fit']} calls={summary['calls']} tok={summary['input_tokens']}+{summary['output_tokens']}"
              f" judge={summary['judge_seconds']}s failed={summary['failed_calls']}", flush=True)

if __name__ == "__main__":
    main()
