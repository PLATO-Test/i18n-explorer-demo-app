# Phase 1 vs phase 2 comparison - run 20260923-v2

Inputs (all under `../i18n-qa/artifacts/20260923-v2/`):

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
| D10 | plural | deterministic | yes | yes | yes |
| G01 | terminology | both | yes | yes | yes |
| G02 | terminology | both | yes | yes | yes |
| G03 | terminology | both | yes | yes | yes |
| G04 | register | both | yes | yes | yes |
| A01 | mistranslation | ai | no | yes | yes |
| A02 | mistranslation | ai | no | yes | yes |
| A03 | mistranslation | ai | no | yes | yes |
| A04 | mistranslation | ai | no | yes | yes |
| A05 | omission | ai | no | yes | yes |
| A06 | image_text | both | yes | yes | yes |
| A07 | image_text | ai | no | yes | yes |
| **total** | | | **15/21** | **16/21** | **21/21** |

## 2. Recall per expected_layer (seeded build)

| approach | deterministic | ai | both | overall |
|---|---|---|---|---|
| deterministic | 10/10 (100%) | 0/6 (0%) | 5/5 (100%) | 15/21 (71%) |
| AI judge | 5/10 (50%) | 6/6 (100%) | 5/5 (100%) | 16/21 (76%) |
| union | 10/10 (100%) | 6/6 (100%) | 5/5 (100%) | 21/21 (100%) |

## 3. False positives

On the seeded build a finding is a false positive only if it lands on a control (a correct element).
Findings that match neither a defect nor a control are "unclassified" and need manual review.
On the clean build nothing is wrong, so every finding is a false positive - except a finding that lands
on a known, pre-existing issue (ground_truth/known_issues.yaml), which counts toward neither.

| approach | seeded: control FPs | seeded: unclassified | seeded: total findings | clean: total findings | clean: known issues | clean: false positives |
|---|---|---|---|---|---|---|
| deterministic | 0 | 0 | 21 | 0 | 0 | 0 |
| AI judge (run 1) | 0 | 0 | 17 | 2 | 1 | 1 |

### Deterministic - seeded build

None.

### Deterministic - clean build

None.

### AI judge (run 1) - seeded build

None.

### AI judge (run 1) - clean build

| scorer class | page | testid | category | observed | expected | description |
|---|---|---|---|---|---|---|
| known issue (U02) | /fr/dashboard | dashboard-recent-transactions-count | terminology | 3 opérations récentes | 3 transactions récentes | The term 'transactions' is translated as 'opérations' here, inconsistent with the heading 'Transactions récentes' used elsewhere on the same page. |
| unclassified | /fr/apply | apply-error-consent | other | Vous devez donner votre accord avant de soumettre. | Vous devez donner votre accord avant de soumettre la demande. | The verb 'soumettre' is used without its object, which sounds incomplete/unnatural in French; it should specify what is being submitted (e.g., 'la demande'). |

The three seeded stability repeats add 0 control FPs and 3 unclassified findings.
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
| D10 | deterministic | 1/3 | yes |
| G01 | both | 3/3 | yes |
| G02 | both | 3/3 | yes |
| G03 | both | 3/3 | yes |
| G04 | both | 3/3 | yes |
| A01 | ai | 3/3 | yes |
| A02 | ai | 3/3 | yes |
| A03 | ai | 3/3 | yes |
| A04 | ai | 3/3 | yes |
| A05 | ai | 3/3 | yes |
| A06 | both | 3/3 | yes |
| A07 | ai | 3/3 | yes |

Defects detected per repeat: 15/21, 16/21, 15/21; mean recall 0.730.

## 5. Calls, tokens, notional cost, duration

Tokens, cost and duration come from each findings file's `run` block. Call counts come from `judge-manifest.json`.
Cost is notional: the CLI reports it on a list-price basis (`costBasis: list`).

| run | calls | input tokens | output tokens | notional cost (USD) | duration (s) |
|---|---|---|---|---|---|
| deterministic, seeded | 0 (no model) | 0 | 0 | $0 | 0.422 |
| deterministic, clean | 0 (no model) | 0 | 0 | $0 | 0.609 |
| AI judge run 1, seeded | 16 jobs / 16 live / 0 cached | 112,172 | 14,092 | $0.4191 | 164.469 |
| AI judge run 1, clean | 16 jobs / 16 live / 0 cached | 110,671 | 8,451 | $0.3521 | 124.469 |
| AI judge run 2, seeded (repeat) | 16 jobs / 16 live / 0 cached | 111,435 | 16,106 | $0.4322 | 186.266 |
| AI judge run 3, seeded (repeat) | 16 jobs / 16 live / 0 cached | 120,439 | 14,495 | $0.4264 | 172.657 |
| AI judge run 4, seeded (repeat) | 16 jobs / 16 live / 0 cached | 103,615 | 12,840 | $0.3907 | 163.391 |

Cost of reaching each single-run result, summed over the live calls of every invocation (including failed attempts) from `calls.json`:

| run | invocations (incl. failed) | live calls | input tokens | output tokens | notional cost (USD) | model time (s) |
|---|---|---|---|---|---|---|
| AI judge run 1, seeded | 1 | 16 | 112,172 | 14,092 | $0.4191 | 164.4 |
| AI judge run 1, clean | 1 | 16 | 110,671 | 8,451 | $0.3521 | 124.3 |

The uncached repeats give the representative cost of one full AI judge pass over 16 jobs: $0.391-$0.432 (mean $0.416), 163-186 s (mean 174 s), about 111,830 input and 14,480 output tokens.

Deterministic makes no model calls. Its duration is check time only.
Snapshot and screenshot capture (`run.json`: seeded 18.532 s, clean 26.563 s) is shared input for both approaches.
It is not charged to either one.
