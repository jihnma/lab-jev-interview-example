# How the applicants' answers were written

Every applicant in `spec.json` is invented. Their answers were written by a language model
(Claude Sonnet 4.5, via subagents) from the row in `spec.json`, one applicant at a time, all
sixteen questions of the plan at once, before any interview ran. The instructions below were
given to the writer verbatim. The answers are in `candidates.json` and were not edited after
an interview had been run on them.

## Instructions given to the writer

You are writing one applicant's answers to all 16 questions of an interview plan. The
applicant is invented. Their row in `spec.json` says what the answers must demonstrate. The
answers are the only thing the interview will ever see, so the row's facts must be visible in
the answers, and nothing beyond them.

Write in the language of the row (`lang`: `ja` → plans/interview-ja.json, `en` →
plans/interview-en.json). Answer every question in the plan, keyed by the question `id`.

**The facts, and how each one shows up:**

- `java`: `none` = never worked on a production Java backend (say so, or talk about something
  else); `thin` = 1–3 years, small role, "the team/senior did it", few own decisions; `solid` =
  4–7 years, owned services, own design decisions with reasons and at least one failure;
  `deep` = 8+ years, several systems, numbers (latency, throughput, incident timelines),
  failures and what changed after them.
- `rust`: `none` = has not written Rust; for rust_hands_on say so plainly; `learning` = no or
  tiny code yet, but a realistic, specific plan (what they have read, what they would build
  first, how long) and a sensible view of boundaries; `hobby` = personal projects with one or
  two specific compiler fights (borrow checker, lifetimes, Send/Sync, tokio) and how they were
  solved; `production` = a real service in Rust, what it did, why Rust, numbers, one failure.
- `money`: `none` = no idempotency / reconciliation / incident work of their own; `textbook` =
  explains idempotency keys, retries, reconciliation and corrections correctly, but every
  example is generic or "at my company we had..." with no numbers, no personal role, no
  failure; `lived` = specific incidents of their own: amounts, counts, durations, what they
  looked at, what the cause was, how it was corrected (new entry, not an edit), what changed
  afterwards.
- `principles`: `aligned` = past behaviour matches the brief's working principles, told as
  concrete episodes (announced and recorded a skipped step in a real emergency, reported own
  mistake early, did on-call and mentoring, argued with data then followed the decision, chose
  a boundary instead of a rewrite); `mixed` = mostly aligned, but the one lapse named in
  `facts.mixed` is told honestly, with regret or with a lesson; `conflict` = the applicant
  clearly and unapologetically shows the behaviour named in `facts.conflict`, in the answers
  where it naturally belongs (see below), while staying technically strong everywhere else.
  The conflict must be stated, not hinted, but told the way a real person would tell it:
  as a story they are comfortable with, not as a confession.
  - `skips_review`: proud of pushing changes without review or outside the deploy procedure
    when there was no emergency, because it was faster (process_skipping, evidence_decision).
  - `hid_incident`: did not report, or delayed reporting, an incident or a mistake and does
    not see the problem with that (incident_response, hiding_and_oncall).
  - `oncall_beneath`: says on-call, support tickets or mentoring juniors are not a senior
    engineer's job (hiding_and_oncall, and it can colour incident_response).
  - `unilateral_rewrite`: rewrote or re-implemented something alone against a team decision
    and is proud of it (evidence_decision, rust_when_not, rust_boundary).
  - `prod_data_testing`: used production data or balances to verify things and sees no
    problem with it (prod_data_verification, money_correctness).
- `style`: `concrete` = specific, numbers, first person; `terse` = short, 40–90 words,
  still specific; `verbose` = 150–250 words, still specific; `vague` = 60–120 words, no
  numbers, no names of systems, "various", "generally", "we made sure", never says what they
  personally did; `persuasive_unsupported` = fluent, confident, well structured, correct
  textbook content, best practices, but never one specific incident of their own — the
  polished answer of someone who has read about it; `irrelevant_drift` = after one or two
  sentences, drifts into impressive but unrelated experience from `background` (a game
  engine, an ML paper, firmware...) and stays there.

**Other rules:**

- Use `background` and `years_backend` for the setting: the domain, the kind of system, the
  scale. Invent consistent details (system names, numbers, dates) and keep them consistent
  across the applicant's 16 answers. Do not name real companies.
- Do not mention the hiring company's name or quote the brief's principles back. A person
  answering does not know the rubric.
- Answers do not know each other: each is a stand-alone answer to that question. The one
  exception is own_contribution, which may refer to "the migration I described" in general
  terms.
- Vary voice between applicants: different openings, different sentence lengths, different
  amounts of hedging. Two applicants with the same facts must not read like the same person.
- Default length 80–160 words (Japanese: 150–350 characters) unless `style` says otherwise.
- Japanese answers: natural spoken-polite Japanese (です・ます), as someone would answer in an
  interview, not written-report style.
- Output: one JSON file per applicant at experiment/answers/<id>.json with the shape
  {"id": "<id>", "answers": {"<question id>": "<answer text>", ...}} containing all 16 ids.
