# Phase 1 vs phase 2 comparison - run 20260922-final

Inputs (all under `../i18n-qa/artifacts/20260922-final/`):

- Phase 1 deterministic: `seeded/findings.json`, `clean/findings.json`
- Phase 2 AI judge, single run: `seeded/findings-ai-judge-1.json`, `clean/findings-ai-judge-1.json`
- Phase 2 AI judge, stability: `seeded/findings-ai-judge-2.json`, `-3.json`, `-4.json` (seeded only, no clean repeats)

All inputs were scored in memory with `scoring.report.build_report`, the same code behind `scoring.score`.
The "AI judge" columns in sections 1-3 are single run 1. Repeats appear only in section 4.

## 1. Per-defect detection (seeded build)

| id | category | expected_layer | deterministic | AI judge | union |
|---|---|---|---|---|---|
| D01 | missing_translation | deterministic | yes | yes | yes |
| D02 | placeholder | deterministic | yes | yes | yes |
| D03 | hardcoded_text | deterministic | yes | yes | yes |
| D04 | truncation | deterministic | yes | no | yes |
| D05 | number_currency_format | deterministic | yes | no | yes |
| D06 | date_format | deterministic | yes | no | yes |
| D07 | lang_attribute | deterministic | yes | no | yes |
| D08 | locale_navigation | deterministic | yes | no | yes |
| D09 | untranslated_validation | deterministic | yes | yes | yes |
| D10 | plural | deterministic | yes | no | yes |
| G01 | terminology | both | yes | yes | yes |
| G02 | terminology | both | yes | yes | yes |
| G03 | terminology | both | yes | yes | yes |
| G04 | register | both | yes | yes | yes |
| A01 | mistranslation | ai | no | yes | yes |
| A02 | mistranslation | ai | no | yes | yes |
| A03 | mistranslation | ai | no | yes | yes |
| A04 | mistranslation | ai | no | yes | yes |
| A05 | omission | ai | no | yes | yes |
| A06 | image_text | ai | yes | yes | yes |
| **total** | | | **15/20** | **14/20** | **20/20** |

## 2. Recall per expected_layer (seeded build)

| approach | deterministic | ai | both | overall |
|---|---|---|---|---|
| deterministic | 10/10 (100%) | 1/6 (17%) | 4/4 (100%) | 15/20 (75%) |
| AI judge | 4/10 (40%) | 6/6 (100%) | 4/4 (100%) | 14/20 (70%) |
| union | 10/10 (100%) | 6/6 (100%) | 4/4 (100%) | 20/20 (100%) |

## 3. False positives

On the seeded build a finding is a false positive only if it lands on a control (a correct element).
Findings that match neither a defect nor a control are "unclassified" and need manual review.
On the clean build nothing is wrong, so every finding is a false positive.

| approach | seeded: control FPs | seeded: unclassified | seeded: total findings | clean: findings (all FP) |
|---|---|---|---|---|
| deterministic | 0 | 0 | 21 | 0 |
| AI judge (run 1) | 0 | 0 | 14 | 2 |

### Deterministic - seeded build

None.

### Deterministic - clean build

None.

### AI judge (run 1) - seeded build

None.

### AI judge (run 1) - clean build

| scorer class | page | testid | category | observed | expected | description |
|---|---|---|---|---|---|---|
| control FP (C08b) | /fr/dashboard | dashboard-recent-transactions-count | terminology | 3 opérations récentes | 3 transactions récentes | Inconsistent terminology: the heading uses 'Transactions récentes' but this element uses 'opérations' for the same English word 'transactions'. |
| unclassified | /fr/calculator | calculator-early-repayment-note | other | Aucuns frais ne s'appliquent au remboursement anticipé. | Aucun frais ne s'applique au remboursement anticipé. | Grammatical error: 'aucun' should remain singular before 'frais', and the verb should agree in the singular ('s'applique'), not plural. |

The three seeded stability repeats add 0 control FPs and 0 unclassified findings.
No clean-build repeats were run, so the clean FP rate of the AI judge rests on one run.

## 4. Stability across the 3 AI judge repeats (seeded build)

Source: `findings-ai-judge-2/3/4.json` (cache bypassed, every call live).
Deterministic is a single run of a deterministic check, so no repeat stability is reported for it.

| id | expected_layer | detected in | AI judge run 1 |
|---|---|---|---|
| D01 | deterministic | 3/3 | yes |
| D02 | deterministic | 3/3 | yes |
| D03 | deterministic | 3/3 | yes |
| D04 | deterministic | 0/3 | no |
| D05 | deterministic | 0/3 | no |
| D06 | deterministic | 0/3 | no |
| D07 | deterministic | 0/3 | no |
| D08 | deterministic | 0/3 | no |
| D09 | deterministic | 3/3 | yes |
| D10 | deterministic | 1/3 | no |
| G01 | both | 3/3 | yes |
| G02 | both | 3/3 | yes |
| G03 | both | 3/3 | yes |
| G04 | both | 3/3 | yes |
| A01 | ai | 3/3 | yes |
| A02 | ai | 3/3 | yes |
| A03 | ai | 3/3 | yes |
| A04 | ai | 3/3 | yes |
| A05 | ai | 3/3 | yes |
| A06 | ai | 3/3 | yes |

Defects detected per repeat: 14/20, 14/20, 15/20; mean recall 0.717.

## 5. Calls, tokens, notional cost, duration

Tokens, cost and duration come from each findings file's `run` block. Call counts come from `judge-manifest.json`.
Cost is notional: the CLI reports it on a list-price basis (`costBasis: list`).

| run | calls | input tokens | output tokens | notional cost (USD) | duration (s) |
|---|---|---|---|---|---|
| deterministic, seeded | 0 (no model) | 0 | 0 | $0 | 0.156 |
| deterministic, clean | 0 (no model) | 0 | 0 | $0 | 0.141 |
| AI judge run 1, seeded | 16 jobs / 6 live / 10 cached | 58,413 | 3,399 | $0.1526 | 48.891 |
| AI judge run 1, clean | 16 jobs / 1 live / 15 cached | 8,953 | 496 | $0.0228 | 8.734 |
| AI judge run 2, seeded (repeat) | 16 jobs / 16 live / 0 cached | 100,765 | 11,760 | $0.3696 | 150.140 |
| AI judge run 3, seeded (repeat) | 16 jobs / 16 live / 0 cached | 100,724 | 11,437 | $0.3662 | 137.250 |
| AI judge run 4, seeded (repeat) | 16 jobs / 16 live / 0 cached | 109,414 | 14,645 | $0.4081 | 176.719 |

**The run-1 `run` blocks understate the real cost.** Both single runs were resumed after failed attempts,
and they reused cached responses from those attempts. The `run` block counts only the final invocation's live calls
(seeded: 6 of 16; clean: 1 of 16). The cost of reaching each single-run result, summed over the live calls of
every invocation from `calls.json`:

| run | invocations (incl. failed) | live calls | input tokens | output tokens | notional cost (USD) | model time (s) |
|---|---|---|---|---|---|---|
| AI judge run 1, seeded | 3 | 18 | 100,748 | 11,624 | $0.3748 | 140.4 |
| AI judge run 1, clean | 2 | 17 | 101,012 | 7,243 | $0.3251 | 119.3 |

The uncached repeats give the representative cost of one full AI judge pass over 16 jobs: $0.366-$0.408 (mean $0.381), 137-177 s (mean 155 s), about 103,634 input and 12,614 output tokens.

Deterministic makes no model calls. Its duration is check time only.
Snapshot and screenshot capture (`run.json`: seeded 18.422 s, clean 18.641 s) is shared input for both approaches.
It is not charged to either one.
