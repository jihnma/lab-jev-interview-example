"""Every number in the README, recomputed from the logs and the records.

    python3 experiment/analyse.py            # all arms found in experiment/logs/
    python3 experiment/analyse.py jev baseline

The arithmetic for a decision (`side`), the fitted bar (`calibrate`, `accuracy`) and the
per-turn choice set (`COVERAGE`) is imported from the program, not copied.
"""
import collections, json, os, pathlib, statistics, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
PROGRAM = pathlib.Path(os.environ.get("PROGRAM", REPO.parent / "lab-jev-interview")).resolve()
sys.path.insert(0, str(PROGRAM))
_cwd = os.getcwd()
os.chdir(PROGRAM)
from core import side, calibrate, accuracy, COVERAGE  # noqa: E402
os.chdir(_cwd)

BAR = 1.5                                  # interface.json's untuned measurement_boundary
SPEC = json.loads((HERE / "spec.json").read_text())
ROWS = {r["id"]: r for r in SPEC["candidates"]}
ORDER = SPEC["order"]
PLANS = {lang: json.loads((REPO / "plans" / f"interview-{lang}.json").read_text()) for lang in ("ja", "en")}
# Unsuffixed arms only by default: a repeat (jev-rep2) or a side run (baseline-thinking) covers
# a few applicants and would shrink the intersection every table is computed on.
ARMS = sys.argv[1:] or sorted(p.stem for p in (HERE / "logs").glob("*.jsonl") if "-" not in p.stem)

def load(arm):
    """The last log row per applicant, plus the record it names."""
    rows = {}
    for line in (HERE / "logs" / f"{arm}.jsonl").read_text().splitlines():
        r = json.loads(line)
        r["record_json"] = json.loads((REPO / "results" / arm / r["record"]).read_text())
        rows[r["id"]] = r
    return rows

def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 2) if xs else None

def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.fmean(xs), 2) if xs else None

def pct(a, b):
    return f"{(a - b) / b * 100:+.1f}%" if b else "n/a"

def table(header, rows):
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join("---" for _ in header) + "|")
    for row in rows:
        print("| " + " | ".join(str(c) for c in row) + " |")
    print()

def per_turn(record, lang):
    """How many questions each turn was chosen from, recomputed from the plan and the order."""
    plan = PLANS[lang]
    asking = {q["id"]: q for q in plan["questions"]}
    dims = [d["name"] for d in plan["dimensions"]]
    policy = plan["policy"]
    order = [r["qid"] for r in record["answers"]]
    out = []
    for turn in range(len(order)):
        asked = order[:turn]
        counts = {d: sum(1 for q in asked if asking[q]["dimension"] == d) for d in dims}
        short = [d for d in dims if counts[d] < policy["per_dimension"]]
        remaining = [q for q in asking if q not in asked]
        narrowed = COVERAGE[plan["coverage"]](remaining, asking, {
            "short": short, "owed": sum(policy["per_dimension"] - counts[d] for d in short),
            "turns_left": policy["max_q"] - len(asked), "head_start": policy["reserve_early"]})
        out.append(len(narrowed) if turn else 1)     # the first question is the plan's own
    return out

def decision(r):
    return side(r["total"], BAR)

def main():
    data = {arm: load(arm) for arm in ARMS}
    ids = sorted(set.intersection(*(set(d) for d in data.values())))
    print(f"arms: {ARMS}; applicants present in every arm: {len(ids)}\n")

    # ── resources ─────────────────────────────────────────────────────
    print("## Resources per interview\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        rows.append([arm, len(d),
                     sum(r["calls"] for r in d), med([r["calls"] for r in d]),
                     sum(r["input_tokens"] for r in d), sum(r["output_tokens"] for r in d),
                     sum(r["input_tokens"] + r["output_tokens"] for r in d),
                     med([r["input_tokens"] + r["output_tokens"] for r in d]),
                     min(r["input_tokens"] + r["output_tokens"] for r in d),
                     max(r["input_tokens"] + r["output_tokens"] for r in d),
                     round(sum(r["judge_seconds"] for r in d), 1), med([r["judge_seconds"] for r in d]),
                     round(sum(r["wall_seconds"] for r in d), 1), med([r["wall_seconds"] for r in d]),
                     round(sum(r["cost_usd"] or 0 for r in d), 2)
                     if any(c.get("cost_usd") is not None for r in d for c in r["per_call"])
                     else "-",
                     sum(r["bytes"] for r in d)])
    # The two byte counts are not one measure of one text: the program sends Jev
    # ASCII-escaped JSON and the baseline prompt is UTF-8. They are printed for exactly
    # that reason, because they say how far apart the two token columns really stand.
    table(["arm", "n", "calls", "calls/med", "input tok", "output tok", "total tok", "tok/med", "tok/min", "tok/max",
           "judge s", "judge s/med", "wall s", "wall s/med", "cost $", "req bytes"], rows)
    if len(ARMS) > 1:
        base = "baseline" if "baseline" in ARMS else ARMS[0]
        b = [data[base][i] for i in ids]
        for arm in ARMS:
            if arm == base:
                continue
            a = [data[arm][i] for i in ids]
            for name, key in (("total tokens", lambda r: r["input_tokens"] + r["output_tokens"]),
                              ("input tokens", lambda r: r["input_tokens"]), ("output tokens", lambda r: r["output_tokens"]),
                              ("judge seconds", lambda r: r["judge_seconds"]), ("wall seconds", lambda r: r["wall_seconds"]),
                              ("calls", lambda r: r["calls"])):
                sa, sb = sum(key(r) for r in a), sum(key(r) for r in b)
                print(f"- {arm} vs {base}, {name}: {sa} vs {sb}, {pct(sa, sb)}")
        print()
    print("### Calls by kind (mean per interview)\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        kinds = collections.Counter()
        toks = collections.Counter()
        secs = collections.Counter()
        for r in d:
            for c in r["per_call"]:
                kinds[c["kind"]] += 1
                toks[c["kind"]] += (c.get("input_tokens") or 0) + (c.get("output_tokens") or 0)
                secs[c["kind"]] += c.get("api_seconds", c["seconds"])
        for k in ("turn", "widget", "score"):
            rows.append([arm, k, round(kinds[k] / len(d), 2), round(toks[k] / max(1, kinds[k])),
                         round(secs[k] / max(1, kinds[k]), 2)])
    table(["arm", "kind", "calls/interview", "tokens/call", "seconds/call"], rows)

    # ── the interview's shape ─────────────────────────────────────────
    print("## Interview shape\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        turns = collections.Counter(r["turns"] for r in d)
        early = [r for r in d if r["turns"] < PLANS[r["lang"]]["policy"]["max_q"]]
        sets_ = len({frozenset(r["order"]) for r in d})
        orders = len({tuple(r["order"]) for r in d})
        choice = [n for r in d for n in per_turn(r["record_json"], r["lang"])[1:]]
        rows.append([arm, dict(sorted(turns.items())), len(early), orders, sets_,
                     round(sum(choice) / len(choice), 2), sum(1 for n in choice if n > 1), len(choice)])
    table(["arm", "turns taken", "ended early", "distinct orders", "distinct sets", "mean choice set", "turns with >1 option", "turns judged"], rows)
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        asked = collections.Counter(q for r in d for q in r["order"])
        never = [q["id"] for q in PLANS["ja"]["questions"] if q["id"] not in asked]
        print(f"- {arm}: asked-count per question {dict(asked.most_common())}; never asked: {never}")
        second = collections.Counter(r["order"][1] for r in d)
        print(f"  second question: {dict(second.most_common())}")
    print()

    # ── decisions against the labels ──────────────────────────────────
    print("## Decisions against the labels (bar 1.5, borderline excluded)\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids if ROWS[i]["label"] in ("hire", "reject")]
        right = sum(1 for r in d if decision(r) == {"hire": "pass", "reject": "fail"}[r["label"]])
        false_hire = [r["id"] for r in d if r["label"] == "reject" and decision(r) == "pass"]
        false_reject = [r["id"] for r in d if r["label"] == "hire" and decision(r) == "fail"]
        unscored = [r["id"] for r in d if r["total"] is None]
        rows.append([arm, len(d), right, f"{right / len(d):.0%}", len(false_hire), len(false_reject), len(unscored)])
        print(f"- {arm}: false hires {false_hire}; false rejects {false_reject}; unscored {unscored}")
    print()
    table(["arm", "labelled", "correct", "accuracy", "false hires", "false rejects", "unscored"], rows)

    print("### With a fit gate (post hoc: pass needs total >= 1.5 AND fit >= 1.5)\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids if ROWS[i]["label"] in ("hire", "reject")]
        gated = lambda r: "pass" if decision(r) == "pass" and (r["fit"] or 0) >= BAR else "fail"
        right = sum(1 for r in d if gated(r) == {"hire": "pass", "reject": "fail"}[r["label"]])
        false_hire = [r["id"] for r in d if r["label"] == "reject" and gated(r) == "pass"]
        false_reject = [r["id"] for r in d if r["label"] == "hire" and gated(r) == "fail"]
        rows.append([arm, len(d), right, f"{right / len(d):.0%}", false_hire, false_reject])
    table(["arm", "labelled", "correct", "accuracy", "false hires", "false rejects"], rows)

    print("### By applicant type\n")
    types = sorted({ROWS[i]["type"] for i in ids})
    rows = []
    for t in types:
        row = [t, ROWS[next(i for i in ids if ROWS[i]["type"] == t)]["label"] if len({ROWS[i]["label"] for i in ids if ROWS[i]["type"] == t}) == 1 else "mixed"]
        for arm in ARMS:
            d = [data[arm][i] for i in ids if ROWS[i]["type"] == t]
            labelled = [r for r in d if r["label"] != "borderline"]
            right = sum(1 for r in labelled if decision(r) == {"hire": "pass", "reject": "fail"}[r["label"]])
            row += [f"{right}/{len(labelled)}" if labelled else "-", med([r["total"] for r in d]), med([r["fit"] for r in d]),
                    collections.Counter(decision(r) for r in d).most_common(1)[0][0] if not labelled else ""]
        rows.append(row)
    table(["type", "label"] + [f"{arm} {c}" for arm in ARMS for c in ("right", "total/med", "fit/med", "borderline→")], rows)

    print("### By language\n")
    rows = []
    for lang in ("ja", "en"):
        for arm in ARMS:
            d = [data[arm][i] for i in ids if ROWS[i]["lang"] == lang]
            labelled = [r for r in d if r["label"] != "borderline"]
            right = sum(1 for r in labelled if decision(r) == {"hire": "pass", "reject": "fail"}[r["label"]])
            rows.append([lang, arm, len(d), f"{right}/{len(labelled)}", f"{right / len(labelled):.0%}",
                         med([r["input_tokens"] + r["output_tokens"] for r in d]), med([r["judge_seconds"] for r in d]),
                         med([r["turns"] for r in d])])
    table(["lang", "arm", "n", "correct", "accuracy", "tok/med", "judge s/med", "turns/med"], rows)

    print("### The values dimension, conflict versus aligned\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        values = lambda r: r["dimensions"].get(PLANS[r["lang"]]["dimensions"][3]["name"])
        for p in ("aligned", "mixed", "conflict"):
            g = [r for r in d if ROWS[r["id"]]["facts"]["principles"] == p]
            rows.append([arm, p, len(g), med([values(r) for r in g]), med([r["fit"] for r in g]), med([r["total"] for r in g]),
                         sum(1 for r in g if decision(r) == "pass"),
                         # `fit` is the one judgement made against the whole brief, so
                         # count how far down it puts a conflict, and how far up a hire.
                         sum(1 for r in g if (r["fit"] or 0) < 1.0),
                         sum(1 for r in g if (r["fit"] or 0) >= BAR)])
    table(["arm", "principles", "n", "values dim/med", "fit/med", "total/med",
           "passed at 1.5", "fit < 1.0", f"fit >= {BAR}"], rows)

    print("### `fit` on the applicants the rule labelled hire\n")
    rows = [[arm, len(g), sum(1 for r in g if (r["fit"] or 0) >= BAR),
             sum(1 for r in g if (r["fit"] or 0) < 1.0), med([r["fit"] for r in g])]
            for arm in ARMS
            for g in [[data[arm][i] for i in ids if ROWS[i]["label"] == "hire"]]]
    table(["arm", "hires", f"fit >= {BAR}", "fit < 1.0", "fit/med"], rows)

    # ── how well each judge ranks, with no bar in it ──────────────────
    # A bar is a second decision on top of the judge, and the untuned 1.5 is nobody's
    # tuned bar. AUC asks only the judge's question: pick one hire and one reject at
    # random, how often does the judge put the hire higher? A tie counts half.
    def auc(value, group):
        pos = [value(r) for r in group if ROWS[r["id"]]["label"] == "hire"]
        neg = [value(r) for r in group if ROWS[r["id"]]["label"] == "reject"]
        if not pos or not neg:
            return None
        return round(sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg)), 3)

    print("### Ranking quality, with no bar (AUC over the labelled applicants)\n")
    rows = []
    for arm in ARMS:
        g = [data[arm][i] for i in ids if ROWS[i]["label"] != "borderline"]
        hires = sorted(r["total"] for r in g if ROWS[r["id"]]["label"] == "hire")
        rejects = sorted(r["total"] for r in g if ROWS[r["id"]]["label"] == "reject")
        # The overlap is what the AUC is made of, in a form a reader can picture.
        over = [r for r in g if ROWS[r["id"]]["label"] == "reject" and r["total"] >= hires[0]]
        rows.append([arm, len(g), auc(lambda r: r["total"], g), auc(lambda r: r["fit"], g),
                     hires[0], rejects[-1], len(over),
                     # Which rejects those are is the whole difference between the judges, so
                     # name them: one arm's set may sit inside another's.
                     "/".join(sorted({ROWS[r["id"]]["type"] for r in over})) or "-",
                     sorted(r["id"] for r in over) or "-"])
    table(["arm", "labelled", "total AUC", "fit AUC", "lowest hire", "highest reject",
           "rejects at or above the lowest hire", "their type", "which"], rows)

    print("### Each thing the brief asks for, as its own dimension\n")
    # The two plans share dimension order, ids and weights, and only the names are
    # translated, so a dimension is taken by position and not by name.
    weights = [d["weight"] for d in PLANS["en"]["dimensions"]]
    assert weights == [d["weight"] for d in PLANS["ja"]["dimensions"]], "plans disagree on weights"
    dim = lambda r, k: r["dimensions"][PLANS[r["lang"]]["dimensions"][k]["name"]]
    rows = []
    for k, weight in enumerate(weights):
        row = [PLANS["en"]["dimensions"][k]["name"], weight]
        for arm in ARMS:
            g = [data[arm][i] for i in ids if ROWS[i]["label"] != "borderline"]
            row += [med([dim(r, k) for r in g if ROWS[r["id"]]["label"] == "hire"]),
                    med([dim(r, k) for r in g if ROWS[r["id"]]["label"] == "reject"]),
                    auc(lambda r: dim(r, k), g)]
        rows.append(row)
    table(["dimension", "weight"] + [f"{a} {w}" for a in ARMS for w in ("hire/med", "reject/med", "AUC")],
          rows)

    print("### The bar fitted to the filed decisions (leave-one-out)\n")
    rows = []
    for arm in ARMS:
        decided = [(data[arm][i]["total"], {"hire": "pass", "reject": "fail"}[ROWS[i]["label"]])
                   for i in ORDER if i in ids and ROWS[i]["label"] != "borderline" and data[arm][i]["total"] is not None]
        fit = calibrate(decided, BAR)
        held = accuracy(decided, BAR)
        rows.append([arm, fit["n"], fit["bar"], fit["span"], fit["wrong"], fit["at_current"],
                     f"{held['right']}/{held['n']} = {held['rate']}", held["chance"]])
    table(["arm", "decided", "best bar", "span", "wrong at best", "wrong at 1.5", "leave-one-out", "chance"], rows)

    # ── across the sequence ───────────────────────────────────────────
    print("## Across the 100-interview sequence\n")
    print("### Early half versus late half (by interview order)\n")
    rows = []
    for arm in ARMS:
        seq = [i for i in ORDER if i in ids]
        for name, part in (("first half", seq[:len(seq) // 2]), ("second half", seq[len(seq) // 2:])):
            d = [data[arm][i] for i in part]
            labelled = [r for r in d if r["label"] != "borderline"]
            right = sum(1 for r in labelled if decision(r) == {"hire": "pass", "reject": "fail"}[r["label"]])
            rows.append([arm, name, len(d), f"{right}/{len(labelled)}", med([r["total"] for r in d]),
                         med([r["turns"] for r in d]), med([r["input_tokens"] + r["output_tokens"] for r in d])])
    table(["arm", "half", "n", "correct", "total/med", "turns/med", "tok/med"], rows)

    print("### The fitted bar as decisions accumulate (the one cross-interview channel)\n")
    rows = []
    for arm in ARMS:
        seq = [i for i in ORDER if i in ids and ROWS[i]["label"] != "borderline" and data[arm][i]["total"] is not None]
        for n in range(10, len(seq) + 1, 10):
            decided = [(data[arm][i]["total"], {"hire": "pass", "reject": "fail"}[ROWS[i]["label"]]) for i in seq[:n]]
            fit = calibrate(decided, BAR)
            rows.append([arm, n, fit["bar"], fit["span"], fit["wrong"], fit["usable"]])
    table(["arm", "decisions so far", "best bar", "span", "wrong", "usable"], rows)

    # ── agreement between arms ────────────────────────────────────────
    if len(ARMS) > 1:
        print("## Agreement between arms\n")
        for k, a in enumerate(ARMS):
            for b in ARMS[k + 1:]:
                same = sum(1 for i in ids if decision(data[a][i]) == decision(data[b][i]))
                xs = [data[a][i]["total"] for i in ids if data[a][i]["total"] is not None and data[b][i]["total"] is not None]
                ys = [data[b][i]["total"] for i in ids if data[a][i]["total"] is not None and data[b][i]["total"] is not None]
                r = statistics.correlation(xs, ys) if len(xs) > 2 else None
                same_order = sum(1 for i in ids if data[a][i]["order"] == data[b][i]["order"])
                same_set = sum(1 for i in ids if set(data[a][i]["order"]) == set(data[b][i]["order"]))
                diff = [(i, ROWS[i]["type"], ROWS[i]["label"], data[a][i]["total"], data[b][i]["total"])
                        for i in ids if decision(data[a][i]) != decision(data[b][i])]
                print(f"- {a} vs {b}: same decision at 1.5 on {same}/{len(ids)}; total correlation r={r and round(r, 3)};"
                      f" identical question order {same_order}/{len(ids)}, identical question set {same_set}/{len(ids)}")
                print(f"  disagreements (id, type, label, {a} total, {b} total): {diff}")
        print()

    # ── errors and flags ──────────────────────────────────────────────
    print("## Errors and flags\n")
    rows = []
    for arm in ARMS:
        d = [data[arm][i] for i in ids]
        flags = collections.Counter(f for r in d for f in r["flags"])
        invalid = sum(c.get("invalid", 0) for r in d for c in r["per_call"])
        retried = sum(1 for r in d for c in r["per_call"] if c.get("attempts", 1) > 1)
        rows.append([arm, sum(r["failed_calls"] for r in d), retried, invalid, sum(1 for r in d if not r["scored"]), dict(flags)])
    table(["arm", "failed calls", "calls retried", "invalid choices", "unscored interviews", "flags"], rows)

    # ── length ────────────────────────────────────────────────────────
    print("## Answer length versus level\n")
    for arm in ARMS:
        pairs = [(len(row["answer"]), row["score"]) for i in ids for row in data[arm][i]["record_json"]["answers"] if row["score"] is not None]
        r = statistics.correlation([p[0] for p in pairs], [p[1] for p in pairs])
        print(f"- {arm}: r = {r:.2f} over {len(pairs)} scored answers")
    print()

    # ── side runs: a handful of applicants under one changed setting ──
    # These are too few to join the tables above, and they are the only record of what
    # the changed setting did, so each one is reported against the same applicants in
    # the arm it varies.
    for side, base in (("baseline-thinking", "baseline"),):
        path = HERE / "logs" / f"{side}.jsonl"
        if not path.is_file() or base not in ARMS:
            continue
        run = load(side)
        common = sorted(set(run) & set(data[base]))
        if not common:
            continue
        print(f"## {side}: {len(common)} of the {base} applicants, one setting changed\n")
        table(["id", f"{side} judge s", f"{base} judge s", f"{side} output tok",
               f"{base} output tok", f"{side} total", f"{base} total"],
              [[i, run[i]["judge_seconds"], data[base][i]["judge_seconds"],
                run[i]["output_tokens"], data[base][i]["output_tokens"],
                run[i]["total"], data[base][i]["total"]] for i in common])

    # ── repeats ───────────────────────────────────────────────────────
    reps = sorted(p.stem for p in (HERE / "logs").glob("*-rep*.jsonl"))
    if reps:
        print("## Repeated interviews (stability, and position in the sequence)\n")
        rows = []
        for arm in ARMS:
            runs = [data[arm]] + [load(rep) for rep in reps if rep.startswith(arm + "-rep")]
            if len(runs) < 2:
                continue
            common = sorted(set.intersection(*(set(r) for r in runs)))
            flips = sum(1 for i in common if len({decision(r[i]) for r in runs}) > 1)
            spread = mean([statistics.pstdev([r[i]["total"] for r in runs if r[i]["total"] is not None]) for i in common])
            same_order = sum(1 for i in common if len({tuple(r[i]["order"]) for r in runs}) == 1)
            same_turns = sum(1 for i in common if len({r[i]["turns"] for r in runs}) == 1)
            rows.append([arm, len(runs), len(common), flips, spread, same_order, same_turns,
                         [(i, [r[i]["total"] for r in runs]) for i in common if len({decision(r[i]) for r in runs}) > 1]])
        table(["arm", "runs", "applicants", "decision flips", "total sd/mean", "same order", "same turns", "which flipped"], rows)

if __name__ == "__main__":
    main()
