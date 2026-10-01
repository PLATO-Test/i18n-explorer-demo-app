# Sonnet 5.5: POC explorer and plugin vs earlier groups

Three seeded runs of the POC explorer and three of plugin 0.1.0, all on `claude-sonnet-5-5` (2026-10-01).
Run setup: `project/05.6-sonnet55-poc.md` and `project/05.6-sonnet55-plugin.md`.
This file compares them with the 23 Sep POC runs 1, 2 and 4, POC control A (Sonnet 5, 29 Sep) and plugin default (Sonnet 5, 28–29 Sep).

## Inputs

| group | run | source | status | model | report |
|---|---|---|---|---|---|
| POC S5.5 | 1, 2, 3 | `../i18n-qa/artifacts/20261001-sonnet55/seeded/findings-ai-explorer-{1,2,3}.json` | completed (manifest and findings `run.status`) | `model_pinned` and `run.model` `claude-sonnet-5-5` | `poc-run-1/`, `poc-run-2/`, `poc-run-3/` |
| POC S5.5 | 1–3 together | same three files | | | `poc-stability/` |
| plugin S5.5 | 1 | `../i18n-explorer/i18n-explorer-runs/20261001-125644-localhost-5002/findings.json` | completed; CLI `success` | `model_configured` `claude-sonnet-5-5`; 61 of 61 subagent assistant entries on it | `plugin-run-1/` |
| plugin S5.5 | 2 | `…/20261001-125823-localhost-5002/findings.json` | completed; CLI `success` | same; 66 of 66 | `plugin-run-2/` |
| plugin S5.5 | 3 | `…/20261001-125955-localhost-5002/findings.json` | completed; CLI `success` | same; 72 of 72 | `plugin-run-3/` |
| plugin S5.5 | 1–3 together | the three converted files | | | `plugin-stability/` |

- `20261001-125414-failed-attempt` was not scored: no model turn ran (05.6-plugin § 4).
- POC `model_usage` lists `claude-haiku-4-5-20251001` next to `claude-sonnet-5-5` in every run: 929 input and 15 output tokens, the same in each. The 23 Sep and control A manifests list Haiku the same way. The plugin's `modelUsage` lists only `claude-sonnet-5-5`.
- The POC files were scored with `scoring.score --build seeded`, as in phase 3.
- The plugin files were converted with `scoring.adapters.plugin_v1` (output kept as `plugin-run-N/findings.converted.json`), then scored the same way.
- The stability reports score each group's three files together.
- The six source files' SHA-256 matched 05.6 before scoring and were unchanged after.
- The earlier groups come from `../20260929-poc-control/A-run-1..3/` and `../20260928-plugin-v0.1.0/seeded/`, `seeded-run-2/`, `seeded-run-3/`.
- The 23 Sep runs were re-scored outside the repo, with the same command. The totals (19, 18, 18) and per-defect results match `../20260929-poc-control/comparison.md`.

**Code baselines.** The POC S5.5 runs used a worktree of `0663db9`, the control B commit, with only `MODEL` changed (05.6-poc § 3). Control A ran at `1b6b61a`.
- Control A is in the tables, as requested.
- Control B (`0663db9`, Sonnet 5) is the code-identical baseline. It is given in the recall table and in § 6.

## 1. Per-defect detection (seeded build)

"POC 23" is the 23 Sep POC runs 1, 2 and 4. "A" is POC control A. "def" is plugin default. "P55" is POC S5.5 and "G55" is plugin S5.5.

| id | category | POC 23 1 | POC 23 2 | POC 23 4 | A 1 | A 2 | A 3 | def 1 | def 2 | def 3 | P55 1 | P55 2 | P55 3 | G55 1 | G55 2 | G55 3 | POC 23 | A | def | P55 | G55 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D02 | placeholder | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D04 | truncation | no | no | no | yes | no | no | no | no | yes | no | no | no | no | no | no | 0/3 | 1/3 | 1/3 | 0/3 | 0/3 |
| D05 | number_currency_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D06 | date_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D07 | lang_attribute | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| D08 | locale_navigation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D10 | plural | yes | yes | yes | no | no | no | no | no | no | yes | yes | yes | yes | yes | yes | 3/3 | 0/3 | 0/3 | 3/3 | 3/3 |
| G01 | terminology | yes | no | no | yes | no | yes | no | no | no | yes | yes | yes | no | yes | no | 1/3 | 2/3 | 0/3 | 3/3 | 1/3 |
| G02 | terminology | yes | yes | yes | yes | no | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| G03 | terminology | yes | yes | yes | yes | yes | yes | no | no | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 |
| G04 | register | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A01 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A02 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A03 | mistranslation | yes | yes | yes | no | no | no | yes | yes | no | yes | yes | yes | no | no | yes | 3/3 | 0/3 | 2/3 | 3/3 | 1/3 |
| A04 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A05 | omission | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A06 | image_text | yes | yes | yes | yes | yes | yes | no | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| A07 | image_text | yes | yes | yes | yes | yes | yes | yes | no | yes | yes | yes | yes | no | no | yes | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 |
| **total** | | **19** | **18** | **18** | **18** | **15** | **16** | **15** | **15** | **17** | **19** | **19** | **19** | **16** | **17** | **18** | | | | | |

### Recall per run

| group | model | run 1 | run 2 | third run (POC 23 Sep: run 4) | range | mean |
|---|---|---|---|---|---|---|
| POC 23 Sep | Sonnet 5 | 19 (0.905) | 18 (0.857) | 18 (0.857) | 18–19 | 18.3 (0.873) |
| POC control A (`1b6b61a`) | Sonnet 5 | 18 (0.857) | 15 (0.714) | 16 (0.762) | 15–18 | 16.3 (0.778) |
| POC control B (`0663db9`), for reference | Sonnet 5 | 16 (0.762) | 17 (0.810) | 15 (0.714) | 15–17 | 16.0 (0.762) |
| plugin default | Sonnet 5 | 15 (0.714) | 15 (0.714) | 17 (0.810) | 15–17 | 15.7 (0.746) |
| **POC S5.5** (`0663db9` + model) | Sonnet 5.5 | 19 (0.905) | 19 (0.905) | 19 (0.905) | 19–19 | 19.0 (0.905) |
| **plugin S5.5** | Sonnet 5.5 | 16 (0.762) | 17 (0.810) | 18 (0.857) | 16–18 | 17.0 (0.810) |

### Found in every run, some runs, none

| group | every run | some runs | no run |
|---|---|---|---|
| POC S5.5 | 19 | none | 2: D04, D07 |
| plugin S5.5 | 16 | 3: G01, A03, A07 (1/3 each) | 2: D04, D07 |

- POC S5.5 found the same 19 defects in all three runs.
- D04 and D07 were missed in all six S5.5 runs. The 23 Sep POC also missed them in every run.

## 2. D10, G03, A03 and the zero-plural rule in the Sonnet 5.5 runs

| id | P55 1 | P55 2 | P55 3 | G55 1 | G55 2 | G55 3 |
|---|---|---|---|---|---|---|
| D10 | found | found | found | found | found | found |
| G03 | found | found | found | found | found | found |
| A03 | found | found | found | missed: examined; named only in another finding's description | missed: examined but not reported | found |
| zero-plural rule | handled | handled | handled | handled | handled | handled |

Method, from each run's `trajectory.jsonl`, the same as in `../20260929-poc-control/comparison.md` § 2:
- **Reached:** a row whose page path (`path`, or `path_before` for in-page tools) is the defect's French page.
- **Examined:** a `read_page`, `inspect` or `page_info` call on that page whose `result` contains the seeded text. In every POC row, `result_chars` equals the length of `result`.
- **Reported:** a `report_finding` call on the defect's element. This method has one difference from the earlier one, explained below the table.

| id | page | run | reached (rows) | examining call | screenshots of the page | report_finding on the element |
|---|---|---|---|---|---|---|
| D10 | `/fr/dashboard` | P55 1 | 2, from seq 35 | seq 35 `read_page` | none | seq 40 |
| D10 | `/fr/dashboard` | P55 2 | 2, from seq 44 | seq 44 `read_page` | none | seq 50 |
| D10 | `/fr/dashboard` | P55 3 | 2, from seq 44 | seq 44 `read_page` | none | seq 50 |
| D10 | `/fr/dashboard` | G55 1 | 7, from seq 45 | seq 45 `read_page` | none | seq 49 |
| D10 | `/fr/dashboard` | G55 2 | 7, from seq 33 | seq 33 `read_page` | none | seq 35 |
| D10 | `/fr/dashboard` | G55 3 | 7, from seq 32 | seq 32 `read_page` | none | seq 34 |
| G03 | `/fr/` | P55 1 | 4, from seq 1 | seq 3 `read_page` | none | seq 8 |
| G03 | `/fr/` | P55 2 | 7, from seq 1 | seq 3 `read_page` | seq 10 | seq 8 |
| G03 | `/fr/` | P55 3 | 4, from seq 1 | seq 3 `read_page` | none | seq 8 |
| G03 | `/fr/` | G55 1 | 10, from seq 0 | seq 1 `read_page` | seq 42 | seq 5 |
| G03 | `/fr/` | G55 2 | 4, from seq 0 | seq 1 `read_page` | none | seq 8 |
| G03 | `/fr/` | G55 3 | 4, from seq 0 | seq 1 `read_page` | none | seq 6 |
| A03 | `/fr/dashboard` | P55 1 | 2, from seq 35 | seq 35 `read_page` | none | seq 43 |
| A03 | `/fr/dashboard` | P55 2 | 2, from seq 44 | seq 44 `read_page` | none | seq 52 |
| A03 | `/fr/dashboard` | P55 3 | 2, from seq 44 | seq 44 `read_page` | none | seq 52 |
| A03 | `/fr/dashboard` | G55 1 | 7, from seq 45 | seq 45 `read_page`: `link "Déclaration mensuelle" [testid=dashboard-statement-link] -> #` | none | none (see below) |
| A03 | `/fr/dashboard` | G55 2 | 7, from seq 33 | seq 33 `read_page`: same line | none | none |
| A03 | `/fr/dashboard` | G55 3 | 7, from seq 32 | seq 32 `read_page` | none | seq 40 |

**A03 in G55 1.** The run had no finding on `dashboard-statement-link`.
- The seeded text appears only in the description of the G02 finding at seq 50, which has element `dashboard-balance-label`, `fr_text` "Balance du compte", and the description: `Anglicism "balance"; also "Déclaration mensuelle" should be "Relevé mensuel".`
- The scorer credits that finding to G02.
- The earlier comparisons' "reported" rule also counted a `report_finding` whose arguments contain the seeded text anywhere. Under that rule this case would have been counted as "reported", so it is labelled separately here.

**A03 in G55 2.** No `report_finding` call and no `finish` summary mentions "Déclaration", "statement" or "Relevé".

**Zero-plural rule.** The correct French is "0 prêt actif". The seeded build shows "0 prêts actifs" (D10).

| run | "0 prêts actifs" read (seq) | `/en/dashboard` `read_page` (seq) | reported (seq) | `expected` / `suggested_fix` | description |
|---|---|---|---|---|---|
| P55 1 | 35 | 37 | 40 | "0 prêt actif" | "In French, zero takes the singular form." |
| P55 2 | 44 | 46 | 50 | "0 prêt actif" | same |
| P55 3 | 44 | 46 | 50 | "0 prêt actif" | "In French, zero takes the singular form; plural used for 0." |
| G55 1 | 45 | none | 49 | "0 prêt actif" | "In French, zero takes the singular." |
| G55 2 | 33 | 40 (after the report) | 35 | "0 prêt actif" | same |
| G55 3 | 32 | 39 (after the report) | 34 | "0 prêt actif" | same |

All six runs state the rule and give the correct singular form.

## 3. Precision and findings that match no defect

| run | findings | matched a defect | control false positive | unclassified | known issue | precision |
|---|---|---|---|---|---|---|
| P55 1 | 22 | 19 | 1 (C01) | 0 | 2 (U03, U04) | 0.950 |
| P55 2 | 21 | 19 | 0 | 0 | 2 (U03, U06) | 1.000 |
| P55 3 | 20 | 19 | 0 | 0 | 1 (U03) | 1.000 |
| G55 1 | 16 | 16 | 0 | 0 | 0 | 1.000 |
| G55 2 | 17 | 17 | 0 | 0 | 0 | 1.000 |
| G55 3 | 18 | 18 | 0 | 0 | 0 | 1.000 |

- Precision is matched ÷ (findings − known-issue findings).
- The scorer's `false_positive_count` adds control false positives and unclassified findings together, so it is 1 in P55 1 and 0 in P55 2.
- Every matched finding hit a different defect. No run has two findings on one defect.
- For comparison, all nine earlier runs in this file (POC 23 Sep, control A, plugin default) have precision 1.000. Their only non-defect findings are U03 hits, one in each 23 Sep run.

The findings that match no defect, as written in the findings files:

| run | matched | page | testid | category / severity | observed | expected | description |
|---|---|---|---|---|---|---|---|
| P55 1 | control C01 (false positive) | `/fr/calculator` | `calculator-apply-now` | terminology / low | Faites votre demande dès maintenant | Faites une demande dès maintenant | Minor: awkward; low priority. (Acceptable but longer than the English "Apply now".) |
| P55 1 | known issue U04 | `/fr/calculator` | `calculator-recalculate-button` | other / low | Calculateur de prêt | Calculer / Recalculer | The action button reuses the page title as its label instead of an action verb (same flaw in English, "Loan calculator"). |
| P55 2 | known issue U06 | `/fr/calculator` | `calculator-modal` | mistranslation / low | notre taux variable fixe | notre taux variable fixe — reformulate e.g. "notre taux variable en vigueur" | Literal translation "taux variable fixe" is self-contradictory in French (variable fixed rate). |
| P55 1 | known issue U03 | `/fr/nonexistent` | – | missing_translation / low | Not Found / The requested URL was not found on the server. … | Page introuvable (French error page with link back to /fr/) | The 404 page under /fr/ is the default English server page, with no French text or navigation. |
| P55 2 | known issue U03 | `/fr/nonexistent` | – | missing_translation / low | Not Found — The requested URL was not found on the server. … | Page introuvable — French 404 page | The 404 page under /fr/ is generic English with no French content or navigation. |
| P55 3 | known issue U03 | `/fr/nonexistent` | – | missing_translation / low | 404 Not Found / "The requested URL was not found on the server. …" | French 404 page within site layout | The 404 page under /fr/ is a generic English server error page. |

The P55 2 finding credited to U06:
- The text it quotes is in `translations/fr.json` (`calculator.modal_body`: "… notre taux variable fixe …"). The English source in `translations/en.json` reads "our fixed variable rate".
- `modal_body` has no entry in `translations/seeded/fr.overrides.json`, so the wording is the same in the clean and seeded builds.
- The English source and the French both contradict themselves, so it is a source-copy problem, not a translation error. It was unclassified when first scored and is now known issue U06 in `known_issues.yaml`, which matches on `calculator-modal` (the modal body paragraph has no testid).

## 4. Behaviour per run

| group | run | effort | model turns (API calls) | budget turns | tool calls | tool calls per turn | thinking tokens | output tokens | duration, harness session (s) | duration, first tool call → `finish` (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| POC 23 Sep | 1 | not set (SDK defaults) | 22 | 21 | 79 | 3.76 | 1,344 | 10,275 | 106.4 | 101.8 |
| POC 23 Sep | 2 | not set | 18 | 18 | 74 | 4.11 | 801 | 8,629 | 90.5 | 86.8 |
| POC 23 Sep | 4 | not set | 20 | 19 | 76 | 4.00 | 984 | 9,671 | 126.0 | 101.6 |
| POC control A | 1 | not set | 66 | 65 | 98 | 1.51 | 7,363 | 19,153 | 230.9 | 217.6 |
| POC control A | 2 | not set | 66 | 65 | 90 | 1.38 | 5,659 | 16,101 | 187.9 | 184.7 |
| POC control A | 3 | not set | 46 | 46 | 103 | 2.24 | 5,219 | 16,092 | 237.0 | 226.7 |
| plugin default | 1 | high | 64 | – | 86 | 1.38 | 4,051 | 17,542 | – | 209.4 (`start_run` → `finish`) |
| plugin default | 2 | high | 44 | – | 84 | 1.98 | 4,294 | 17,757 | – | 244.0 |
| plugin default | 3 | high | 76 | – | 99 | 1.33 | 5,871 | 21,683 | – | 274.7 |
| **POC S5.5** | 1 | not set (SDK defaults) | 21 | 20 | 75 | 3.75 | 1,047 | 10,001 | 129.5 | 102.9 |
| **POC S5.5** | 2 | not set | 23 | 23 | 80 | 3.48 | 872 | 9,432 | 92.1 | 86.2 |
| **POC S5.5** | 3 | not set | 22 | 21 | 77 | 3.67 | 971 | 9,774 | 83.6 | 78.0 |
| **plugin S5.5** | 1 | medium | 17 | – | 51 | 3.25 | 462 | 8,844 | – | 75.7 (`start_run` → `finish`) |
| **plugin S5.5** | 2 | medium | 16 | – | 55 | 3.73 | 468 | 9,892 | – | 71.8 |
| **plugin S5.5** | 3 | medium | 17 | – | 58 | 3.69 | 494 | 10,659 | – | 81.0 |

| group | model turns | tool calls per turn | thinking tokens | output tokens | duration, first tool call → `finish` (s) |
|---|---|---|---|---|---|
| POC 23 Sep | 18–22 | 3.76–4.11 | 801–1,344 | 8,629–10,275 | 86.8–101.8 |
| POC control A | 46–66 | 1.38–2.24 | 5,219–7,363 | 16,092–19,153 | 184.7–226.7 |
| POC control B | 46–61 | 1.77–2.09 | 3,672–6,432 | 15,669–17,725 | 178.6–223.6 |
| plugin default | 44–76 | 1.33–1.98 | 4,051–5,871 | 17,542–21,683 | 209.4–274.7 |
| POC S5.5 | 21–23 | 3.48–3.75 | 872–1,047 | 9,432–10,001 | 78.0–102.9 |
| plugin S5.5 | 16–17 | 3.25–3.73 | 462–494 | 8,844–10,659 | 71.8–81.0 |

**Effort.**
- **Plugin S5.5:** every explorer assistant entry carries `"effort":"medium","perTurnEffort":"medium"` (05.6-plugin § 5).
- **Plugin default:** recorded `"effort":"high"` (05.4).
- **POC, every group:** sets no effort. The manifest records `thinking_effort: "SDK defaults (not set)"`, and nothing in the POC artifacts records the level the CLI applied.

Definitions. These are the same as `../20260929-poc-control/comparison.md` § 3, whose figures for the earlier groups are reused here.
- **Model turns:** API calls.
  - POC: CLI `status: requesting` events in `transcript.jsonl`.
  - Plugin: distinct `message.id` in the subagent transcript.
  - 05.6-poc's "model turns" row is the budget-turns column here (20 / 23 / 21).
- **Budget turns:** the POC manifest's `budget_used.turns`. The plugin has no such counter.
- **Tool calls:** the budget counter. POC: `budget_used.tool_calls`. Plugin: the trajectory's budget count, which excludes `start_run`.
- **Tool calls per turn:**
  - POC: tool calls ÷ budget turns.
  - Plugin: tool calls including `start_run` ÷ (API calls − 1). This gives 3.25 / 3.73 / 3.69.
  - 05.6-plugin divides by API calls instead (3.06 / 3.50 / 3.47).
- **Thinking tokens:** `model_usage[<agent model>].thinkingTokens` (plugin: `modelUsage`).
- **Output tokens:** POC: the manifest's `tokens.output_tokens`. In P55 2 it is 3 above `result_usage.output_tokens` (9,429). Plugin: `modelUsage.outputTokens`.
- **Duration:** POC: `manifest.duration_s` and first trajectory row → `finish`. Plugin: `start_run` → `finish` in the trajectory, which equals the run's `duration_s`. The CLI's `duration_ms` was 80.3 / 78.3 / 88.0 s.

Other recorded differences for the plugin, Sonnet 5 default → Sonnet 5.5:
- Claude Code CLI 2.1.284 → 2.1.286.
- `maxOutputTokens` 64,000 → 128,000.
- The plugin was loaded from the repo's install → `--plugin-dir` on a temporary copy of tag `v0.1.0`.

For the POC, the S5.5 runs and control B share SDK 0.2.158, CLI 2.1.280 and the code at `0663db9`. The only difference between them is `MODEL`. The CLI recorded `maxOutputTokens` 128,000 for `claude-sonnet-5-5`.

## 5. Statements

**(a) Sonnet 5.5 vs Sonnet 5 today.**

- **POC:**
  - **Recall:** 19 in all three S5.5 runs, against control A 15–18 (mean 16.3) and control B 15–17 (mean 16.0). The ranges do not overlap.
  - **Per defect:** D10 was found in 3/3 S5.5 runs vs 0/3 in A and 0/3 in B. A03 was found in 3/3 vs 0/3 (A) and 1/3 (B).
  - **Code:** S5.5 and control B differ only in the model constant.
  - **Behaviour:** model turns 21–23 vs 46–66, tool calls per turn 3.48–3.75 vs 1.38–2.24, thinking tokens 872–1,047 vs 3,672–7,363, output tokens 9,432–10,001 vs 15,669–19,153. A and B are taken together in each comparison, and none of the ranges overlap.
  - **Against 23 Sep:** recall 19 vs 18–19, and the same 19 defects as 23 Sep run 1. Model turns, thinking tokens and output tokens overlap the 23 Sep ranges. Tool calls per turn (3.48–3.75) sits just below 23 Sep's 3.76–4.11.
  - **Precision:** 0.950, 1.000, 1.000 vs 1.000 in every control A run. The one non-1.000 run has one control false positive (C01).
- **Plugin:**
  - **Recall:** S5.5 16–18 (mean 17.0) vs default 15–17 (mean 15.7). The ranges overlap at 16–17.
  - **Per defect:** D10 3/3 vs 0/3, G03 3/3 vs 1/3, G01 1/3 vs 0/3, A03 1/3 vs 2/3, A07 1/3 vs 2/3.
  - **Behaviour:** model turns 16–17 vs 44–76, tool calls per turn 3.25–3.73 vs 1.33–1.98, thinking tokens 462–494 vs 4,051–5,871, output tokens 8,844–10,659 vs 17,542–21,683, duration 71.8–81.0 s vs 209.4–274.7 s. None of the ranges overlap.
  - **Other recorded differences:** the model is not the only one. Effort (high → medium), CLI version, `maxOutputTokens` and the plugin load path also changed (§ 4). The data does not separate their effects.
  - **Precision:** 1.000 in both groups.

**(b) POC vs plugin on Sonnet 5.5.**
- **Recall:** POC 19/19/19 vs plugin 16–18. The ranges do not overlap.
- **Per defect:** the POC found every defect the plugin found. G01, A03 and A07 were found in 3/3 POC runs and 1/3 plugin runs. All other defects are equal.
  - Both found D10 and G03 in 3/3 runs, and both missed D04 and D07 in 3/3.
  - Each plugin miss of A03 had the text in a `read_page` result.
- **Precision:** the POC scored 0.950, 1.000 and 1.000, the plugin 1.000 in all three runs.
- **Behaviour:**
  - Thinking tokens (POC 872–1,047 vs plugin 462–494) do not overlap. Neither do model turns (21–23 vs 16–17).
  - Tool calls per turn (3.48–3.75 vs 3.25–3.73) and output tokens (9,432–10,001 vs 8,844–10,659) overlap.
  - Tool calls are 75–80 vs 51–58.
- **Effort:** the plugin recorded effort medium. The POC sets no effort and records no level, so whether the two ran at different effort levels cannot be told from this data.
- **Other setup differences:** prompt, tools and runtime differ between the two, as listed in 05.4. The CLI is 2.1.280 for the POC and 2.1.286 for the plugin. `maxOutputTokens` is 128,000 in both.
- None of the differences above is attributed to a cause.

## 6. Notes

- `project/05.6-sonnet55-poc.md` reports `costBasis: "unknown"` and `contextWindow: 200000` for `claude-sonnet-5-5` in the POC. The plugin's CLI (2.1.286) reports `costBasis: "list"` and `contextWindow: 1000000`. Neither figure is used here.
- The POC S5.5 runs each have one U03 hit, as the 23 Sep runs did. Control A had none.
