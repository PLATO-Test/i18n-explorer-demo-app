# Phase 1 vs phase 2 vs phase 3 comparison - run 20260923-v2

Inputs (all under `../i18n-qa/artifacts/20260923-v2/`):

- Phase 1 deterministic: `seeded/findings.json`, `clean/findings.json`
- Phase 2 AI judge, single run: `seeded/findings-ai-judge-1.json`, `clean/findings-ai-judge-1.json`
- Phase 2 AI judge, stability: `seeded/findings-ai-judge-2.json`, `-3.json`, `-4.json` (seeded only, no clean repeats)
- Phase 3 AI explorer, single run: `seeded/findings-ai-explorer-1.json`, `clean/findings-ai-explorer-1.json`
- Phase 3 AI explorer, stability: `seeded/findings-ai-explorer-1.json`, `-2.json`, `-4.json` (seeded only, complete runs only, no clean repeats)
- Phase 3 AI explorer, per-run manifests and coverage: `seeded/explorer/<n>/manifest.json`, `coverage.json`

All inputs were scored in memory with `scoring.report.build_report`, the same code behind `scoring.score`.
The "AI judge" columns in sections 1-3 are single run 1 and the "AI explorer" columns single run 1. Repeats appear only in section 4.

## 1. Per-defect detection (seeded build)

| id | category | expected_layer | deterministic | AI judge | AI explorer | union of all three |
|---|---|---|---|---|---|---|
| D01 | missing_translation | deterministic | yes | yes | yes | yes |
| D02 | placeholder | deterministic | yes | yes | yes | yes |
| D03 | hardcoded_text | deterministic | yes | yes | yes | yes |
| D04 | truncation | deterministic | yes | no | no | yes |
| D05 | number_currency_format | deterministic | yes | no | yes | yes |
| D06 | date_format | deterministic | yes | no | yes | yes |
| D07 | lang_attribute | deterministic | yes | no | no | yes |
| D08 | locale_navigation | deterministic | yes | no | yes | yes |
| D09 | untranslated_validation | deterministic | yes | yes | yes | yes |
| D10 | plural | deterministic | yes | yes | yes | yes |
| G01 | terminology | both | yes | yes | yes | yes |
| G02 | terminology | both | yes | yes | yes | yes |
| G03 | terminology | both | yes | yes | yes | yes |
| G04 | register | both | yes | yes | yes | yes |
| A01 | mistranslation | ai | no | yes | yes | yes |
| A02 | mistranslation | ai | no | yes | yes | yes |
| A03 | mistranslation | ai | no | yes | yes | yes |
| A04 | mistranslation | ai | no | yes | yes | yes |
| A05 | omission | ai | no | yes | yes | yes |
| A06 | image_text | both | yes | yes | yes | yes |
| A07 | image_text | ai | no | yes | yes | yes |
| **total** | | | **15/21** | **16/21** | **19/21** | **21/21** |

Defects found by exactly one approach:

| approach | only this approach found |
|---|---|
| deterministic | D04, D07 |
| AI judge | none |
| AI explorer | none |
| none of the three | none |

## 2. Recall per expected_layer (seeded build)

| approach | deterministic | ai | both | overall |
|---|---|---|---|---|
| deterministic | 10/10 (100%) | 0/6 (0%) | 5/5 (100%) | 15/21 (71%) |
| AI judge | 5/10 (50%) | 6/6 (100%) | 5/5 (100%) | 16/21 (76%) |
| AI explorer | 8/10 (80%) | 6/6 (100%) | 5/5 (100%) | 19/21 (90%) |
| union of all three | 10/10 (100%) | 6/6 (100%) | 5/5 (100%) | 21/21 (100%) |

## 3. False positives

On the seeded build a finding is a false positive only if it lands on a control (a correct element).
Findings that match neither a defect nor a control are "unclassified" and need manual review.
On the clean build nothing is wrong, so every finding is a false positive - except a finding that lands
on a known, pre-existing issue (ground_truth/known_issues.yaml), which counts toward neither.

| approach | seeded: control FPs | seeded: known issues | seeded: unclassified | seeded: total findings | clean: total findings | clean: known issues | clean: false positives |
|---|---|---|---|---|---|---|---|
| deterministic | 0 | 0 | 0 | 21 | 0 | 0 | 0 |
| AI judge (run 1) | 0 | 0 | 0 | 17 | 2 | 1 | 1 |
| AI explorer (run 1) | 0 | 1 | 0 | 20 | 2 | 2 | 0 |

Known-issue hits by id (single runs):

| approach | build | U01 | U02 | U03 | U04 |
|---|---|---|---|---|---|
| deterministic | seeded | 0 | 0 | 0 | 0 |
| deterministic | clean | 0 | 0 | 0 | 0 |
| AI judge (run 1) | seeded | 0 | 0 | 0 | 0 |
| AI judge (run 1) | clean | 0 | 1 | 0 | 0 |
| AI explorer (run 1) | seeded | 0 | 0 | 1 | 0 |
| AI explorer (run 1) | clean | 0 | 0 | 1 | 1 |

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

### AI explorer (run 1) - seeded build

| scorer class | page | testid | category | observed | expected | description |
|---|---|---|---|---|---|---|
| known issue (U03) | /fr/nonexistent | - | missing_translation | 404 Not Found / "The requested URL was not found on the server..." | Localized French 404 page (e.g. "Page introuvable") | The 404 page under /fr/ is the default English server error page. |

### AI explorer (run 1) - clean build

| scorer class | page | testid | category | observed | expected | description |
|---|---|---|---|---|---|---|
| known issue (U03) | /fr/nonexistent | - | missing_translation | Title "404 Not Found"; heading "Not Found"; "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." | Localized French 404 page, e.g. "Page introuvable" with a French explanation | Unknown URLs under /fr/ show the default English server 404 page, without site header, and with no French translation. |
| known issue (U04) | /fr/calculator | calculator-recalculate-button | mistranslation | Button label "Calculateur de prêt" (same as the page title) | "Recalculer" or "Calculer le paiement" | The form submit button carries the page-title text instead of an action verb (the test id suggests "recalculate"). The English also reuses "Loan calculator", but the French button reads as a noun rather than an action. |

The three seeded stability repeats add 0 control FPs and 3 unclassified findings.
No clean-build repeats were run, so the clean FP rate of the AI judge rests on one run.

Across all three seeded AI explorer runs (single run 1 included): 0 control FPs, 0 unclassified findings and 3 known-issue hits. The clean FP rate of the AI explorer rests on one run.

## 4. Stability: AI judge (3 repeats) and AI explorer (3 complete runs), seeded build

AI judge source: `findings-ai-judge-2/3/4.json` (cache bypassed, every call live).
AI explorer source: `findings-ai-explorer-1/2/4.json`, all with manifest status `completed`. Explorer runs that did not complete (a rate-limited run) are scored separately and excluded here.
Deterministic is a single run of a deterministic check, so no repeat stability is reported for it.

| id | expected_layer | AI judge detected in (repeats) | AI judge run 1 | AI explorer detected in (runs 1/2/4) |
|---|---|---|---|---|
| D01 | deterministic | 3/3 | yes | 3/3 |
| D02 | deterministic | 3/3 | yes | 3/3 |
| D03 | deterministic | 3/3 | yes | 3/3 |
| D04 | deterministic | 0/3 | no | 0/3 |
| D05 | deterministic | 0/3 | no | 3/3 |
| D06 | deterministic | 0/3 | no | 3/3 |
| D07 | deterministic | 0/3 | no | 0/3 |
| D08 | deterministic | 0/3 | no | 3/3 |
| D09 | deterministic | 3/3 | yes | 3/3 |
| D10 | deterministic | 1/3 | yes | 3/3 |
| G01 | both | 3/3 | yes | 1/3 |
| G02 | both | 3/3 | yes | 3/3 |
| G03 | both | 3/3 | yes | 3/3 |
| G04 | both | 3/3 | yes | 3/3 |
| A01 | ai | 3/3 | yes | 3/3 |
| A02 | ai | 3/3 | yes | 3/3 |
| A03 | ai | 3/3 | yes | 3/3 |
| A04 | ai | 3/3 | yes | 3/3 |
| A05 | ai | 3/3 | yes | 3/3 |
| A06 | both | 3/3 | yes | 3/3 |
| A07 | ai | 3/3 | yes | 3/3 |

AI judge defects detected per repeat: 15/21, 16/21, 15/21; mean recall 0.730.

AI explorer defects detected per run: 19/21, 18/21, 18/21; mean recall 0.873.
Found in every run: 18. Found in some but not all runs: G01. Never found: D04, D07.

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
Snapshot and screenshot capture (`run.json`: seeded 18.532 s, clean 26.563 s) is shared input for deterministic and AI judge.
It is not charged to either one. The AI explorer browses the live app instead and does not use it.

### AI explorer: calls, tokens, notional cost, duration

Tokens, cost and duration come from each findings file's `run` block, and status, model turns, tool calls and
screenshots from `explorer/<n>/manifest.json`. "input total" is the `run` block's `input_tokens`: fresh input,
cache reads and cache writes of all models used (the pinned model and a small Haiku helper), summed. The three
parts come from the manifest's `model_usage`, which is also the source of the `run` block and the cost.
Model turns are assistant turns (one model call each). Tool calls are the browser tool calls the agent made.

| run | status | model turns | tool calls | screenshots | input total | cache read | cache write | fresh input | output tokens | notional cost (USD) | duration (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| seeded run 1 (single run) | completed | 21 | 79 | 4 | 420,674 | 386,046 | 33,657 | 971 | 10,290 | $0.3157 | 106.4 |
| clean run 1 (single run) | completed | 21 | 76 | 2 | 401,558 | 369,044 | 31,543 | 971 | 6,523 | $0.2662 | 85.8 |
| seeded run 2 (stability) | completed | 18 | 74 | 4 | 292,012 | 261,565 | 29,484 | 963 | 8,620 | $0.2574 | 90.5 |
| seeded run 4 (stability) | completed | 19 | 76 | 2 | 359,585 | 324,493 | 34,125 | 967 | 9,686 | $0.2992 | 126.0 |
| seeded run 3 (excluded from stability) | rate_limited | 7 | 32 | 1 | 58,532 | 48,017 | 9,572 | 943 | 3,300 | $0.0818 | 34.8 |

Cost basis reported by the harness: `list price, notional on a subscription`.

Note: 4 of 4 runs above report `interrupted: true` together with `finish_called: true` (and `result_subtype: error_during_execution`). This is expected harness behaviour: the wind-down stops the session after the agent calls `finish`. It is not a failed run.

Note: for seeded run 2 (stability), the manifest's per-turn token totals (325,070 input tokens) exceed its `model_usage` for the pinned model (291,083). The table uses `model_usage`, the source of the `run` block and of the reported cost, so nothing here confirms it. If the per-turn totals are the right ones, this run's input tokens are 33,987 higher and its cost is understated too.

### AI explorer: pages covered per locale

From `explorer/<n>/coverage.json`: pages reached / pages in the page map, and configured states reached /
configured states. `coverage.json` describes its own method as a post-run proxy from the trajectory.

| run | en pages | fr pages | en states | fr states |
|---|---|---|---|---|
| seeded run 1 (single run) | 4/5 | 5/5 | 6/10 | 8/10 |
| clean run 1 (single run) | 4/5 | 5/5 | 6/10 | 9/10 |
| seeded run 2 (stability) | 4/5 | 5/5 | 5/10 | 8/10 |
| seeded run 4 (stability) | 4/5 | 5/5 | 5/10 | 8/10 |

Note: in 4 of 4 runs above, `coverage.json` lists a page as never visited although `visited_paths_not_in_config` holds a path of that page (the English application summary, whose page map has no path). The proxy does not credit that visit, so the page count for that locale is one too low.

### One pass per approach

Mean over the runs used for stability, seeded build: deterministic is a single run, the AI judge is its 3 repeats, the AI explorer is its three complete runs.

| approach | model calls | tool calls | input tokens | output tokens | notional cost (USD) | duration (s) |
|---|---|---|---|---|---|---|
| deterministic | 0 | - | 0 | 0 | $0 | 0.422 |
| AI judge | 16 | - | 111,830 | 14,480 | $0.416 | 174 |
| AI explorer | 19 | 76 | 357,424 | 9,532 | $0.291 | 108 |

AI judge model calls are live calls per pass. AI explorer model calls are assistant turns.
