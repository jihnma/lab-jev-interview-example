arms: ['baseline', 'jev', 'jev1']; applicants present in every arm: 100

## Resources per interview

| arm | n | calls | calls/med | input tok | output tok | total tok | tok/med | tok/min | tok/max | judge s | judge s/med | wall s | wall s/med | cost $ | req bytes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 100 | 2150 | 24.0 | 14781757 | 308471 | 15090228 | 154040.5 | 105079 | 189584 | 3893.4 | 40.38 | 6663.4 | 70.41 | 30.86 | 48437515 |
| jev | 100 | 4460 | 46.0 | 32244530 | 479770 | 32724300 | 322110.0 | 228544 | 407114 | 994.7 | 10.13 | 995.7 | 10.14 | - | 163983093 |
| jev1 | 100 | 2138 | 22.0 | 14336600 | 180485 | 14517085 | 145075.0 | 92918 | 182793 | 475.3 | 4.9 | 475.8 | 4.9 | - | 72651448 |

- jev vs baseline, total tokens: 32724300 vs 15090228, +116.9%
- jev vs baseline, input tokens: 32244530 vs 14781757, +118.1%
- jev vs baseline, output tokens: 479770 vs 308471, +55.5%
- jev vs baseline, judge seconds: 994.73 vs 3893.37, -74.5%
- jev vs baseline, wall seconds: 995.71 vs 6663.37, -85.1%
- jev vs baseline, calls: 4460 vs 2150, +107.4%
- jev1 vs baseline, total tokens: 14517085 vs 15090228, -3.8%
- jev1 vs baseline, input tokens: 14336600 vs 14781757, -3.0%
- jev1 vs baseline, output tokens: 180485 vs 308471, -41.5%
- jev1 vs baseline, judge seconds: 475.26 vs 3893.37, -87.8%
- jev1 vs baseline, wall seconds: 475.8 vs 6663.37, -92.9%
- jev1 vs baseline, calls: 2138 vs 2150, -0.6%

### Calls by kind (mean per interview)

| arm | kind | calls/interview | tokens/call | seconds/call |
|---|---|---|---|---|
| baseline | turn | 10.75 | 7431 | 2.03 |
| baseline | widget | 9.75 | 5772 | 1.17 |
| baseline | score | 1.0 | 14741 | 5.68 |
| jev | turn | 31.95 | 7232 | 0.22 |
| jev | widget | 9.65 | 5481 | 0.21 |
| jev | score | 3.0 | 14427 | 0.31 |
| jev1 | turn | 10.69 | 7246 | 0.22 |
| jev1 | widget | 9.69 | 5494 | 0.21 |
| jev1 | score | 1.0 | 14472 | 0.32 |

## Interview shape

| arm | turns taken | ended early | distinct orders | distinct sets | mean choice set | turns with >1 option | turns judged |
|---|---|---|---|---|---|---|---|
| baseline | {8: 10, 9: 17, 10: 12, 11: 10, 12: 51} | 49 | 97 | 60 | 10.39 | 975 | 975 |
| jev | {8: 1, 9: 25, 10: 22, 11: 12, 12: 40} | 60 | 92 | 46 | 10.46 | 965 | 965 |
| jev1 | {8: 2, 9: 23, 10: 20, 11: 14, 12: 41} | 59 | 92 | 52 | 10.44 | 969 | 969 |

- baseline: asked-count per question {'java_tx_design': 100, 'money_correctness': 100, 'incident_response': 100, 'java_ops': 97, 'rust_readiness': 97, 'hiding_and_oncall': 95, 'process_skipping': 85, 'rust_boundary': 67, 'java_recovery': 65, 'reconciliation_mismatch': 63, 'own_contribution': 56, 'rust_hands_on': 46, 'evidence_decision': 43, 'rust_when_not': 28, 'prod_data_verification': 21, 'java_perf_change': 12}; never asked: []
  second question: {'money_correctness': 66, 'java_ops': 27, 'own_contribution': 5, 'rust_readiness': 2}
- jev: asked-count per question {'java_tx_design': 100, 'rust_readiness': 99, 'money_correctness': 98, 'hiding_and_oncall': 98, 'rust_boundary': 97, 'java_ops': 97, 'process_skipping': 92, 'rust_hands_on': 71, 'evidence_decision': 66, 'incident_response': 60, 'reconciliation_mismatch': 51, 'java_recovery': 48, 'own_contribution': 37, 'prod_data_verification': 36, 'java_perf_change': 9, 'rust_when_not': 6}; never asked: []
  second question: {'money_correctness': 57, 'own_contribution': 21, 'java_ops': 16, 'reconciliation_mismatch': 4, 'rust_readiness': 1, 'incident_response': 1}
- jev1: asked-count per question {'java_tx_design': 100, 'money_correctness': 99, 'rust_readiness': 99, 'rust_boundary': 97, 'hiding_and_oncall': 97, 'process_skipping': 94, 'java_ops': 94, 'rust_hands_on': 70, 'evidence_decision': 64, 'incident_response': 63, 'reconciliation_mismatch': 54, 'java_recovery': 49, 'own_contribution': 39, 'prod_data_verification': 34, 'java_perf_change': 9, 'rust_when_not': 7}; never asked: []
  second question: {'money_correctness': 57, 'own_contribution': 20, 'java_ops': 18, 'reconciliation_mismatch': 3, 'rust_readiness': 2}

## Decisions against the labels (bar 1.5, borderline excluded)

- baseline: false hires ['c004', 'c019', 'c021', 'c028', 'c035', 'c036', 'c040', 'c042', 'c045', 'c047', 'c050', 'c056', 'c058', 'c060', 'c061', 'c067', 'c069', 'c070', 'c074', 'c089', 'c092', 'c095']; false rejects []; unscored []
- jev: false hires ['c004', 'c014', 'c019', 'c021', 'c028', 'c033', 'c035', 'c036', 'c040', 'c042', 'c045', 'c047', 'c050', 'c056', 'c058', 'c060', 'c061', 'c067', 'c069', 'c070', 'c074', 'c078', 'c084', 'c089', 'c090', 'c092', 'c095', 'c096']; false rejects []; unscored []
- jev1: false hires ['c004', 'c014', 'c019', 'c021', 'c028', 'c033', 'c035', 'c036', 'c040', 'c042', 'c045', 'c047', 'c050', 'c056', 'c058', 'c060', 'c061', 'c067', 'c069', 'c070', 'c074', 'c078', 'c084', 'c089', 'c090', 'c092', 'c095', 'c096']; false rejects []; unscored []

| arm | labelled | correct | accuracy | false hires | false rejects | unscored |
|---|---|---|---|---|---|---|
| baseline | 90 | 68 | 76% | 22 | 0 | 0 |
| jev | 90 | 62 | 69% | 28 | 0 | 0 |
| jev1 | 90 | 62 | 69% | 28 | 0 | 0 |

### With a fit gate (post hoc: pass needs total >= 1.5 AND fit >= 1.5)

| arm | labelled | correct | accuracy | false hires | false rejects |
|---|---|---|---|---|---|
| baseline | 90 | 73 | 81% | ['c019', 'c028', 'c035', 'c036', 'c040', 'c042', 'c045', 'c047', 'c056', 'c060', 'c061', 'c067', 'c070', 'c074', 'c089', 'c092', 'c095'] | [] |
| jev | 90 | 80 | 89% | ['c014', 'c036', 'c045', 'c047', 'c056', 'c067', 'c070', 'c089', 'c090', 'c095'] | [] |
| jev1 | 90 | 80 | 89% | ['c014', 'c036', 'c045', 'c047', 'c056', 'c067', 'c070', 'c089', 'c090', 'c095'] | [] |

### By applicant type

| type | label | baseline right | baseline total/med | baseline fit/med | baseline borderline→ | jev right | jev total/med | jev fit/med | jev borderline→ | jev1 right | jev1 total/med | jev1 fit/med | jev1 borderline→ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| borderline | borderline | - | 2.79 | 2.85 | pass | - | 2.62 | 2.31 | pass | - | 2.65 | 2.34 | pass |
| impressive_irrelevant | reject | 5/6 | 1.12 | 2.02 |  | 4/6 | 1.31 | 1.79 |  | 4/6 | 1.31 | 1.76 |  |
| java_to_rust_potential | hire | 8/8 | 2.99 | 3.0 |  | 8/8 | 2.99 | 2.83 |  | 8/8 | 2.99 | 2.82 |  |
| persuasive_unsupported | reject | 6/6 | 1.33 | 1.31 |  | 3/6 | 1.46 | 1.05 |  | 3/6 | 1.48 | 1.05 |  |
| rust_engineer | mixed | 3/6 | 2.46 | 2.92 |  | 3/6 | 2.5 | 2.54 |  | 3/6 | 2.5 | 2.51 |  |
| strong_both | hire | 22/22 | 2.96 | 2.98 |  | 22/22 | 2.85 | 2.79 |  | 22/22 | 2.84 | 2.79 |  |
| strong_tech_weak_culture | reject | 0/14 | 2.64 | 1.88 |  | 0/14 | 2.32 | 0.04 |  | 0/14 | 2.3 | 0.03 |  |
| vague | reject | 6/6 | 1.17 | 1.28 |  | 5/6 | 1.19 | 1.04 |  | 5/6 | 1.17 | 1.04 |  |
| weak_both | reject | 8/8 | 0.83 | 1.23 |  | 8/8 | 0.83 | 0.55 |  | 8/8 | 0.84 | 0.55 |  |
| weak_tech_strong_culture | reject | 10/14 | 1.41 | 2.18 |  | 9/14 | 1.4 | 1.98 |  | 9/14 | 1.41 | 2.0 |  |

### By language

| lang | arm | n | correct | accuracy | tok/med | judge s/med | turns/med |
|---|---|---|---|---|---|---|---|
| ja | baseline | 60 | 42/53 | 79% | 165683.0 | 42.08 | 12.0 |
| ja | jev | 60 | 39/53 | 74% | 361776.0 | 10.46 | 11.0 |
| ja | jev1 | 60 | 39/53 | 74% | 160703.0 | 4.96 | 11.0 |
| en | baseline | 40 | 26/37 | 70% | 147492.0 | 39.12 | 11.0 |
| en | jev | 40 | 23/37 | 62% | 303703.0 | 9.8 | 10.5 |
| en | jev1 | 40 | 23/37 | 62% | 137204.0 | 4.54 | 10.5 |

### The values dimension, conflict versus aligned

| arm | principles | n | values dim/med | fit/med | total/med | passed at 1.5 | fit < 1.0 | fit >= 1.5 |
|---|---|---|---|---|---|---|---|---|
| baseline | aligned | 73 | 2.83 | 2.85 | 2.48 | 46 | 4 | 61 |
| baseline | mixed | 9 | 2.87 | 2.75 | 2.83 | 5 | 1 | 6 |
| baseline | conflict | 18 | 2.07 | 1.65 | 2.55 | 14 | 6 | 10 |
| jev | aligned | 73 | 2.74 | 2.45 | 2.47 | 52 | 0 | 58 |
| jev | mixed | 9 | 2.41 | 1.64 | 2.62 | 5 | 0 | 5 |
| jev | conflict | 18 | 1.86 | 0.04 | 2.23 | 14 | 18 | 0 |
| jev1 | aligned | 73 | 2.79 | 2.46 | 2.49 | 52 | 0 | 56 |
| jev1 | mixed | 9 | 2.4 | 1.74 | 2.67 | 5 | 0 | 5 |
| jev1 | conflict | 18 | 1.8 | 0.03 | 2.23 | 14 | 18 | 0 |

### `fit` on the applicants the rule labelled hire

| arm | hires | fit >= 1.5 | fit < 1.0 | fit/med |
|---|---|---|---|---|
| baseline | 33 | 33 | 0 | 2.98 |
| jev | 33 | 33 | 0 | 2.79 |
| jev1 | 33 | 33 | 0 | 2.79 |

### Ranking quality, with no bar (AUC over the labelled applicants)

| arm | labelled | total AUC | fit AUC | lowest hire | highest reject | rejects at or above the lowest hire | their type | which |
|---|---|---|---|---|---|---|---|---|
| baseline | 90 | 0.969 | 0.969 | 2.48 | 2.96 | 11 | strong_tech_weak_culture | ['c019', 'c021', 'c028', 'c035', 'c040', 'c042', 'c060', 'c061', 'c069', 'c074', 'c092'] |
| jev | 90 | 0.992 | 0.98 | 2.49 | 2.73 | 4 | strong_tech_weak_culture | ['c019', 'c021', 'c040', 'c092'] |
| jev1 | 90 | 0.993 | 0.982 | 2.51 | 2.74 | 4 | strong_tech_weak_culture | ['c019', 'c021', 'c040', 'c092'] |

### Each thing the brief asks for, as its own dimension

| dimension | weight | baseline hire/med | baseline reject/med | baseline AUC | jev hire/med | jev reject/med | jev AUC | jev1 hire/med | jev1 reject/med | jev1 AUC |
|---|---|---|---|---|---|---|---|---|---|---|
| Java backend practice | 0.28 | 2.99 | 1.08 | 0.902 | 3.0 | 1.02 | 0.906 | 3.0 | 1.0 | 0.896 |
| Rust readiness | 0.16 | 2.94 | 1.42 | 0.903 | 2.91 | 1.39 | 0.884 | 2.91 | 1.41 | 0.88 |
| Money correctness and operational judgment | 0.32 | 3.0 | 1.14 | 0.938 | 2.95 | 1.45 | 0.944 | 2.96 | 1.45 | 0.943 |
| Alignment with how we work | 0.24 | 3.0 | 1.93 | 0.969 | 2.99 | 1.96 | 0.938 | 2.99 | 1.97 | 0.947 |

### The bar fitted to the filed decisions (leave-one-out)

| arm | decided | best bar | span | wrong at best | wrong at 1.5 | leave-one-out | chance |
|---|---|---|---|---|---|---|---|
| baseline | 90 | 2.685 | (2.68, 2.78) | 8 | 22 | 80/90 = 0.889 | 0.633 |
| jev | 90 | 2.4800000000000004 | (2.47, 2.49) | 4 | 28 | 85/90 = 0.944 | 0.633 |
| jev1 | 90 | 2.49 | (2.47, 2.54) | 4 | 28 | 84/90 = 0.933 | 0.633 |

## Across the 100-interview sequence

### Early half versus late half (by interview order)

| arm | half | n | correct | total/med | turns/med | tok/med |
|---|---|---|---|---|---|---|
| baseline | first half | 50 | 33/44 | 2.62 | 11.0 | 151929.5 |
| baseline | second half | 50 | 35/46 | 2.0 | 12.0 | 154219.0 |
| jev | first half | 50 | 31/44 | 2.5 | 10.0 | 323748.5 |
| jev | second half | 50 | 31/46 | 1.96 | 11.0 | 319315.0 |
| jev1 | first half | 50 | 31/44 | 2.5 | 11.0 | 146193.0 |
| jev1 | second half | 50 | 31/46 | 1.96 | 11.0 | 143793.0 |

### The fitted bar as decisions accumulate (the one cross-interview channel)

| arm | decisions so far | best bar | span | wrong | usable |
|---|---|---|---|---|---|
| baseline | 10 | 2.435 | (2.29, 2.58) | 0 | True |
| baseline | 20 | 2.385 | (2.29, 2.48) | 2 | True |
| baseline | 30 | 2.385 | (2.29, 2.58) | 3 | True |
| baseline | 40 | 2.385 | (2.29, 2.58) | 6 | True |
| baseline | 50 | 2.385 | (2.29, 2.58) | 6 | True |
| baseline | 60 | 2.54 | (2.5, 2.85) | 7 | True |
| baseline | 70 | 2.685 | (2.68, 2.78) | 7 | True |
| baseline | 80 | 2.685 | (2.68, 2.78) | 7 | True |
| baseline | 90 | 2.685 | (2.68, 2.78) | 8 | True |
| jev | 10 | 2.34 | (2.14, 2.54) | 0 | True |
| jev | 20 | 2.3150000000000004 | (2.14, 2.77) | 2 | True |
| jev | 30 | 2.3150000000000004 | (2.14, 2.49) | 2 | True |
| jev | 40 | 2.4800000000000004 | (2.47, 2.49) | 3 | True |
| jev | 50 | 2.4800000000000004 | (2.47, 2.49) | 3 | True |
| jev | 60 | 2.4800000000000004 | (2.47, 2.49) | 3 | True |
| jev | 70 | 2.4800000000000004 | (2.47, 2.49) | 3 | True |
| jev | 80 | 2.4800000000000004 | (2.47, 2.49) | 3 | True |
| jev | 90 | 2.4800000000000004 | (2.47, 2.49) | 4 | True |
| jev1 | 10 | 2.35 | (2.16, 2.54) | 0 | True |
| jev1 | 20 | 2.35 | (2.16, 2.78) | 2 | True |
| jev1 | 30 | 2.335 | (2.16, 2.51) | 2 | True |
| jev1 | 40 | 2.49 | (2.47, 2.54) | 3 | True |
| jev1 | 50 | 2.49 | (2.47, 2.54) | 3 | True |
| jev1 | 60 | 2.49 | (2.47, 2.54) | 3 | True |
| jev1 | 70 | 2.49 | (2.47, 2.54) | 3 | True |
| jev1 | 80 | 2.49 | (2.47, 2.54) | 3 | True |
| jev1 | 90 | 2.49 | (2.47, 2.54) | 4 | True |

## Agreement between arms

- baseline vs jev: same decision at 1.5 on 94/100; total correlation r=0.97; identical question order 0/100, identical question set 6/100
  disagreements (id, type, label, baseline total, jev total): [('c014', 'impressive_irrelevant', 'reject', 1.16, 1.89), ('c033', 'persuasive_unsupported', 'reject', 1.32, 1.51), ('c078', 'vague', 'reject', 1.45, 1.6), ('c084', 'persuasive_unsupported', 'reject', 1.37, 1.63), ('c090', 'weak_tech_strong_culture', 'reject', 1.48, 1.56), ('c096', 'persuasive_unsupported', 'reject', 1.35, 1.68)]
- baseline vs jev1: same decision at 1.5 on 94/100; total correlation r=0.969; identical question order 0/100, identical question set 4/100
  disagreements (id, type, label, baseline total, jev1 total): [('c014', 'impressive_irrelevant', 'reject', 1.16, 1.89), ('c033', 'persuasive_unsupported', 'reject', 1.32, 1.5), ('c078', 'vague', 'reject', 1.45, 1.57), ('c084', 'persuasive_unsupported', 'reject', 1.37, 1.5), ('c090', 'weak_tech_strong_culture', 'reject', 1.48, 1.55), ('c096', 'persuasive_unsupported', 'reject', 1.35, 1.66)]
- jev vs jev1: same decision at 1.5 on 100/100; total correlation r=0.999; identical question order 40/100, identical question set 68/100
  disagreements (id, type, label, jev total, jev1 total): []

## Errors and flags

| arm | failed calls | calls retried | invalid choices | unscored interviews | flags |
|---|---|---|---|---|---|
| baseline | 0 | 2 | 0 | 0 | {'tied_levels': 8} |
| jev | 0 | 0 | 0 | 0 | {'tied_levels': 9} |
| jev1 | 0 | 0 | 0 | 0 | {'tied_levels': 10} |

## Answer length versus level

- baseline: r = 0.38 over 1075 scored answers
- jev: r = 0.38 over 1065 scored answers
- jev1: r = 0.38 over 1069 scored answers

## baseline-thinking: 3 of the baseline applicants, one setting changed

| id | baseline-thinking judge s | baseline judge s | baseline-thinking output tok | baseline output tok | baseline-thinking total | baseline total |
|---|---|---|---|---|---|---|
| c002 | 537.42 | 39.82 | 44810 | 2958 | 0.52 | 1.17 |
| c022 | 443.46 | 30.41 | 38639 | 2430 | 2.93 | 2.69 |
| c025 | 397.91 | 28.56 | 33297 | 2400 | 2.88 | 3.0 |

## Repeated interviews (stability, and position in the sequence)

| arm | runs | applicants | decision flips | total sd/mean | same order | same turns | which flipped |
|---|---|---|---|---|---|---|---|
| baseline | 2 | 12 | 0 | 0.03 | 1 | 7 | [] |
| jev | 2 | 12 | 0 | 0.01 | 5 | 11 | [] |

