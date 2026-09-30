"""The 100 applicants: who they are, what their answers demonstrate, and the label each one
carries — fixed here, before any interview ran, and never edited after.

    python3 experiment/make_candidates.py    # writes experiment/spec.json

The label is a rule over the facts and nothing else:

    hire       java in {solid, deep} and money == lived and principles == aligned
    reject     principles == conflict, or java in {none, thin}, or money == none
    borderline everything else (solid Java with only textbook money handling, or a lived
               record with one 'mixed' lapse on the principles)

Rust is left out of the rule on purpose: the brief says it is not required, so it varies
freely across the population and is measured on its own. `facts` describe what the written
answers demonstrate, not what the person "really" is: a vague answerer with a strong career
underneath is still recorded as `thin`, because that is all the interview can see.
"""
import json, pathlib, random

random.seed(20260929)
OUT = pathlib.Path(__file__).parent / "spec.json"

# type -> how many, and the facts they are drawn with. (java, rust, money, principles, style)
TYPES = {
    "strong_both":            (22, ["solid", "deep"], ["none", "learning", "hobby", "production"], ["lived"], ["aligned"], ["concrete", "concrete", "terse", "verbose"]),
    "strong_tech_weak_culture": (14, ["solid", "deep"], ["none", "learning", "hobby", "production"], ["lived"], ["conflict"], ["concrete"]),
    "weak_tech_strong_culture": (14, ["thin", "thin", "thin", "none"], ["none", "learning"], ["textbook", "none"], ["aligned"], ["concrete", "terse"]),
    "weak_both":              (8,  ["thin", "none"], ["none", "learning"], ["none", "textbook"], ["conflict", "mixed"], ["concrete", "vague"]),
    "rust_engineer":          (6,  ["solid", "thin"], ["production"], ["lived", "textbook"], ["aligned"], ["concrete"]),
    "java_to_rust_potential": (8,  ["deep"], ["learning"], ["lived"], ["aligned"], ["concrete"]),
    "impressive_irrelevant":  (6,  ["none", "thin"], ["none", "hobby"], ["none"], ["aligned"], ["irrelevant_drift"]),
    "vague":                  (6,  ["thin"], ["none", "learning"], ["textbook"], ["aligned"], ["vague"]),
    "persuasive_unsupported": (6,  ["thin"], ["learning", "hobby"], ["textbook"], ["aligned"], ["persuasive_unsupported"]),
    "borderline":             (10, ["solid"], ["learning", "hobby"], ["textbook", "lived"], ["aligned", "mixed"], ["concrete"]),
}
CONFLICTS = ["skips_review", "hid_incident", "oncall_beneath", "unilateral_rewrite", "prod_data_testing"]
MIXED = ["delayed a report once, regrets it", "skipped a deploy step in a real emergency and announced it afterwards",
         "reluctant about on-call but does it", "argued a rewrite hard, then accepted the team's no"]
IRRELEVANT = ["game engine lead in C++", "machine-learning researcher in Python", "embedded firmware engineer in C",
              "Android app lead in Kotlin", "data-platform engineer in Scala/Spark", "front-end architect in TypeScript"]
BACKGROUNDS = {
    "ja": ["大手銀行のシステム子会社で勘定系のJava開発", "決済代行会社のバックエンド", "ECモールの注文・決済基盤",
           "証券会社の約定システム", "SaaSスタートアップの課金基盤", "通信キャリアの料金計算システム",
           "ポイントサービスの台帳", "保険会社の契約管理システム", "受託開発会社で複数の業務システム",
           "ゲーム会社の課金・アイテム管理", "物流会社の配送管理", "コンビニ系電子マネーの加盟店精算"],
    "en": ["a payments processor in Singapore", "a neobank in Berlin", "a marketplace settlement team in London",
           "a crypto exchange's ledger team", "an insurance claims platform", "a ride-hailing company's wallet team",
           "a telecom billing system", "an enterprise ERP vendor", "a remittance startup", "an ad-tech bidding platform",
           "a hotel booking payments team", "a public-sector tax system"],
}
YEARS = {"none": [0, 1], "thin": [1, 2, 3], "solid": [4, 5, 6, 7], "deep": [8, 10, 12, 15]}

def label(f):
    if f["principles"] == "conflict" or f["java"] in ("none", "thin") or f["money"] == "none":
        return "reject"
    if f["java"] in ("solid", "deep") and f["money"] == "lived" and f["principles"] == "aligned":
        return "hire"
    return "borderline"

rows = []
for kind, (n, javas, rusts, moneys, principles, styles) in TYPES.items():
    for i in range(n):
        f = {"java": javas[i % len(javas)], "rust": rusts[i % len(rusts)],
             "money": moneys[i % len(moneys)], "principles": principles[i % len(principles)],
             "style": styles[i % len(styles)]}
        if kind == "rust_engineer":            # thin Java goes with textbook money, solid with lived
            f["money"] = "lived" if f["java"] == "solid" else "textbook"
        if kind == "borderline":               # half textbook-money, half mixed-principles, never both
            f["money"], f["principles"] = (["textbook", "aligned"], ["lived", "mixed"])[i % 2]
        if kind == "weak_both" and f["principles"] == "mixed":
            f["principles"] = "conflict" if i % 4 == 0 else "mixed"
        f["conflict"] = CONFLICTS[i % len(CONFLICTS)] if f["principles"] == "conflict" else None
        f["mixed"] = MIXED[i % len(MIXED)] if f["principles"] == "mixed" else None
        rows.append({"type": kind, "facts": f})

random.shuffle(rows)
langs = ["ja"] * 60 + ["en"] * 40
random.shuffle(langs)
for k, (row, lang) in enumerate(zip(rows, langs), 1):
    f = row["facts"]
    row.update({"id": f"c{k:03d}", "lang": lang, "label": label(f),
                "background": (IRRELEVANT[k % len(IRRELEVANT)] if row["type"] == "impressive_irrelevant"
                               else random.choice(BACKGROUNDS[lang])),
                "years_backend": random.choice(YEARS[f["java"]])})

# a fixed interview order, the same for every arm: the shuffled order above, by id
OUT.write_text(json.dumps({"rule": __doc__.split("\n\n")[1].strip(), "order": [r["id"] for r in rows],
                           "candidates": rows}, ensure_ascii=False, indent=1) + "\n")
from collections import Counter
print(len(rows), Counter(r["label"] for r in rows), Counter(r["lang"] for r in rows))
print(Counter((r["type"], r["label"]) for r in rows))
