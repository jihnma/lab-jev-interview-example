"""experiment/answers/<id>.json (one file per applicant, written by the writer) ->
experiment/candidates.json (everything the interviews read: the spec row and the answers)."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
spec = json.loads((HERE / "spec.json").read_text())
plans = {lang: json.loads((HERE.parent / "plans" / f"interview-{lang}.json").read_text()) for lang in ("ja", "en")}
answers = {}
for row in spec["candidates"]:
    written = json.loads((HERE / "answers" / f"{row['id']}.json").read_text())["answers"]
    wanted = {q["id"] for q in plans[row["lang"]]["questions"]}
    assert set(written) == wanted and all(written[q].strip() for q in wanted), row["id"]
    answers[row["id"]] = {q: written[q] for q in wanted}
(HERE / "candidates.json").write_text(json.dumps(
    {"rule": spec["rule"], "order": spec["order"], "candidates": spec["candidates"], "answers": answers},
    ensure_ascii=False, indent=1) + "\n")
print(f"{len(answers)} applicants, {sum(len(a) for a in answers.values())} answers")
