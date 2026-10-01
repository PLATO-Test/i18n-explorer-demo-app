# POC explorer control re-run (2026-09-29) vs POC 23 Sep vs plugin

Control experiment: the phase 3 POC explorer re-run unchanged against the seeded build, 3 times at commit `1b6b61a` (tag `phase3-prompt-v1`, "control A") and 3 times at `0663db9` ("control B").
Setup, commands, versions and the A-vs-B code diff are in `project/05.5-poc-control-rerun.md`.
This file compares the six control runs with the 23 Sep POC runs 1, 2 and 4 and the six plugin 0.1.0 runs (3 default, 3 isolated).

Inputs (all status `completed`, checked in each `manifest.json`):

| group | run | findings file | report |
|---|---|---|---|
| control A | 1, 2, 3 | `../i18n-qa/artifacts/20260929-control-A/seeded/findings-ai-explorer-{1,2,3}.json` | `A-run-1/`, `A-run-2/`, `A-run-3/` |
| control A | 1–3 together | same three files | `A-stability/` |
| control B | 1, 2, 3 | `../i18n-qa/artifacts/20260929-control-B/seeded/findings-ai-explorer-{1,2,3}.json` | `B-run-1/`, `B-run-2/`, `B-run-3/` |
| control B | 1–3 together | same three files | `B-stability/` |
| POC 23 Sep | 1, 2, 4 | `../i18n-qa/artifacts/20260923-v2/seeded/findings-ai-explorer-{1,2,4}.json` | scored with `scoring.report.build_report`, as in `../20260929-plugin-v0.1.0-isolated/comparison.md` |
| plugin default | 1, 2, 3 | | `../20260928-plugin-v0.1.0/seeded/`, `seeded-run-2/`, `seeded-run-3/` |
| plugin isolated | 1, 2, 3 | | `../20260929-plugin-v0.1.0-isolated/run-1/`, `run-2/`, `run-3/` |

- The control findings files in `../i18n-qa/artifacts/` have the same SHA-256 as the originals in the two temporary worktrees.
- Each control file was scored with `scoring.score --build seeded`, the same way as phase 3. No conversion is needed: the POC writes the scorer's format.
- The stability reports score each group's three files together, as for the 23 Sep POC.
- The six findings files had the same checksums before and after scoring.

## 1. Per-defect detection (seeded build)

| id | category | POC 1 | POC 2 | POC 4 | A 1 | A 2 | A 3 | B 1 | B 2 | B 3 | def 1 | def 2 | def 3 | iso 1 | iso 2 | iso 3 | POC | A | B | def | iso |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D02 | placeholder | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D04 | truncation | no | no | no | yes | no | no | yes | no | no | no | no | yes | yes | no | no | 0/3 | 1/3 | 1/3 | 1/3 | 1/3 |
| D05 | number_currency_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D06 | date_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D07 | lang_attribute | no | no | no | no | no | no | no | yes | no | no | no | no | no | no | no | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 |
| D08 | locale_navigation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D10 | plural | yes | yes | yes | no | no | no | no | no | no | no | no | no | no | no | no | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| G01 | terminology | yes | no | no | yes | no | yes | yes | yes | yes | no | no | no | yes | yes | no | 1/3 | 2/3 | 3/3 | 0/3 | 2/3 |
| G02 | terminology | yes | yes | yes | yes | no | no | no | yes | yes | yes | yes | yes | no | yes | no | 3/3 | 1/3 | 2/3 | 3/3 | 1/3 |
| G03 | terminology | yes | yes | yes | yes | yes | yes | no | no | no | no | no | yes | no | no | no | 3/3 | 3/3 | 0/3 | 1/3 | 0/3 |
| G04 | register | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A01 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A02 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A03 | mistranslation | yes | yes | yes | no | no | no | no | yes | no | yes | yes | no | no | no | no | 3/3 | 0/3 | 1/3 | 2/3 | 0/3 |
| A04 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A05 | omission | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A06 | image_text | yes | yes | yes | yes | yes | yes | yes | no | no | no | yes | yes | yes | yes | yes | 3/3 | 3/3 | 1/3 | 2/3 | 3/3 |
| A07 | image_text | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | no | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| **total** | | **19** | **18** | **18** | **18** | **15** | **16** | **16** | **17** | **15** | **15** | **15** | **17** | **16** | **16** | **14** | | | | | |

"POC" is the 23 Sep runs, "A" and "B" are the control runs, "def" is plugin default and "iso" is plugin isolated.

The D04, D07 and A06 hits that are new to the POC explorer were checked against the findings:
- **D04 (A1, B1):** each finding is on `apply-submit-button` and quotes `scrollWidth 290` / `clientWidth 210`.
- **D07 (B2):** the finding reports `html lang="en"` on `/fr/application/AP-100482`, expected `fr-CA`.

### Recall per run

| group | run 1 | run 2 | run 3 (POC: run 4) | range | mean |
|---|---|---|---|---|---|
| POC 23 Sep | 19 (0.905) | 18 (0.857) | 18 (0.857) | 18–19 | 18.3 (0.873) |
| control A | 18 (0.857) | 15 (0.714) | 16 (0.762) | 15–18 | 16.3 (0.778) |
| control B | 16 (0.762) | 17 (0.810) | 15 (0.714) | 15–17 | 16.0 (0.762) |
| plugin default | 15 (0.714) | 15 (0.714) | 17 (0.810) | 15–17 | 15.7 (0.746) |
| plugin isolated | 16 (0.762) | 16 (0.762) | 14 (0.667) | 14–16 | 15.3 (0.730) |

- Of the 6 control runs, 1 (A1, 18) reaches the lowest 23 Sep POC score. The other 5 are below it.
- The control A and B ranges (15–18, 15–17) overlap each other and both plugin ranges (14–16, 15–17).
- Seeded precision is 1.000 in all six control runs. Each run's findings count equals its detected count: every finding matched a different defect. There were no control false positives, no known-issue hits and no unclassified findings.

### Found in every run, some runs, none

| group | every run | some runs | no run |
|---|---|---|---|
| POC 23 Sep | 18 | 1: G01 (1/3) | 2: D04, D07 |
| control A | 15: D01, D02, D03, D05, D06, D08, D09, G03, G04, A01, A02, A04, A05, A06, A07 | 3: G01 (2/3); D04, G02 (1/3) | 3: D07, D10, A03 |
| control B | 14: D01, D02, D03, D05, D06, D08, D09, G01, G04, A01, A02, A04, A05, A07 | 5: G02 (2/3); D04, D07, A03, A06 (1/3) | 2: D10, G03 |
| plugin default | 13 | 5: A03, A06, A07 (2/3); D04, G03 (1/3) | 3: D07, D10, G01 |
| plugin isolated | 14 | 3: G01 (2/3); D04, G02 (1/3) | 4: D07, D10, G03, A03 |

- D10 is the only defect the 23 Sep POC found in every run that no control run found.
- A03 is found in every 23 Sep run and in 1 of 6 control runs. G02 is found in every 23 Sep run and in 3 of 6 control runs.

## 2. D10, G03, A03 and the zero-plural rule in the control runs

| id | A 1 | A 2 | A 3 | B 1 | B 2 | B 3 |
|---|---|---|---|---|---|---|
| D10 | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported |
| G03 | found | found | found | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported |
| A03 | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported | found | missed: examined but not reported |
| zero-plural rule | not handled | not handled | not handled | not handled | not handled | not handled |

Method, from each run's `trajectory.jsonl` (the same as in the plugin comparisons):

- **Reached:** a row whose page path (`path`, or `path_before` for in-page tools) is the defect's French page.
- **Examined:** a `read_page`, `inspect` or `page_info` call on that page whose `result` contains the seeded text.
  - For every row, `result_chars` equals the length of the stored `result`.
- **Reported:** a `report_finding` call whose `data_testid` is the defect's testid or whose arguments contain the seeded text.
- **Screenshots** are listed but not counted as evidence, since they can't be searched.

| id | page | run | reached (rows) | examining call | screenshots of the page | report_finding on the element |
|---|---|---|---|---|---|---|
| D10 | `/fr/dashboard` | A1 | 6, from seq 41 | seq 42 `read_page`: `span "0 prêts actifs" [testid=dashboard-active-loans-count]` | seq 51 | none |
| D10 | `/fr/dashboard` | A2 | 7, from seq 43 | seq 44 `read_page`: same line | none | none |
| D10 | `/fr/dashboard` | A3 | 6, from seq 42 | seq 43 `read_page`: same line | none | none |
| D10 | `/fr/dashboard` | B1 | 2, from seq 33 | seq 34 `read_page`: same line | none | none |
| D10 | `/fr/dashboard` | B2 | 6, from seq 58 | seq 59 `read_page`: same line | seq 106 | none |
| D10 | `/fr/dashboard` | B3 | 9, from seq 37 | seq 38 `read_page`: same line | seq 93 | none |
| G03 | `/fr/` | A1 | 9, from seq 1 | seq 2 `read_page`, seq 90 `inspect` | seq 60 | seq 91 (found) |
| G03 | `/fr/` | A2 | 11, from seq 1 | seq 2, seq 86 `read_page` | seq 78 | seq 87 (found) |
| G03 | `/fr/` | A3 | 9, from seq 1 | seq 2 `read_page` | seq 7 | seq 11 (found) |
| G03 | `/fr/` | B1 | 10, from seq 1 | seq 3 `read_page`: `link "Appliquer pour un prêt" [testid=landing-cta-apply] -> /fr/apply` | seq 7 | none |
| G03 | `/fr/` | B2 | 5, from seq 1 | seq 2 `read_page`: same line | none | none |
| G03 | `/fr/` | B3 | 6, from seq 1 | seq 2 `read_page`: same line | none | none |
| A03 | `/fr/dashboard` | A1 | 6, from seq 41 | seq 42 `read_page`: `link "Déclaration mensuelle" [testid=dashboard-statement-link] -> #` | seq 51 | none |
| A03 | `/fr/dashboard` | A2 | 7, from seq 43 | seq 44 `read_page`: same line | none | none |
| A03 | `/fr/dashboard` | A3 | 6, from seq 42 | seq 43 `read_page`: same line | none | none |
| A03 | `/fr/dashboard` | B1 | 2, from seq 33 | seq 34 `read_page`: same line | none | none |
| A03 | `/fr/dashboard` | B2 | 6, from seq 58 | seq 59 `read_page`: same line | seq 106 | seq 66 (found) |
| A03 | `/fr/dashboard` | B3 | 9, from seq 37 | seq 38 `read_page`: same line | seq 93 | none |

- None of the 14 misses is "not reached" or "reached but not examined". In each, the text was in a `read_page` result on the French page.
- D10 and A03 are in the same `/fr/dashboard` `read_page` result in every run.
- For comparison, the 23 Sep POC runs read the same `/fr/dashboard` text (seq 57, 44, 44) and reported D10 at seq 63, 49, 48 and A03 at seq 65, 52, 50.

### Zero-plural rule (French zero takes the singular)

The correct French text is "0 prêt actif" (CLDR/Babel: `Locale.parse('fr_CA').plural_form(0) == 'one'`). The seeded build shows "0 prêts actifs" (D10).

| run | "0 prêts actifs" read (seq) | `/en/dashboard` read next (seq) | reported | handled correctly? |
|---|---|---|---|---|
| POC 23 Sep 1 / 2 / 4 | 57 / 44 / 44 | 59 / 46 / 46 | yes: seq 63 / 49 / 48 | yes |
| A1 | 42 | 44 | no | no |
| A2 | 44 | 46 | no | no |
| A3 | 43 | 45 | no | no |
| B1 | 34 | 36 | no | no |
| B2 | 59 | 61 | no | no |
| B3 | 38 | 40 | no | no |

- In the control runs, no `report_finding` call and no `finish` summary mentions "plural", "pluriel", "singular", "singulier", "prêt actif" or "active loans".
- Two control runs have visible text blocks (`transcript.jsonl`, `kind: text`) that mention plurals:
  - **A3:** "Now let's check the dashboard "pending application" count text plural rules and check "1 demande en attente" for correctness". It goes on: "Let's check if there's a way to test plural forms with different loan counts (e.g. viewing dashboard with 2 active loans doesn't seem controllable)". It does not name the "0 prêts actifs" text, and no finding followed.
  - **B3:** mentions plural only for the word "mois".
- The thinking blocks have empty text, so the reasoning cannot be seen.

## 3. Behaviour per run

| group | run | model turns | tool calls | tool calls per turn | thinking tokens | output tokens | duration, harness session (s) | duration, first tool call → `finish` (s) |
|---|---|---|---|---|---|---|---|---|
| POC 23 Sep | 1 | 22 | 79 | 3.76 | 1,344 | 10,275 | 106.4 | 101.8 |
| POC 23 Sep | 2 | 18 | 74 | 4.11 | 801 | 8,629 | 90.5 | 86.8 |
| POC 23 Sep | 4 | 20 | 76 | 4.00 | 984 | 9,671 | 126.0 | 101.6 |
| control A | 1 | 66 | 98 | 1.51 | 7,363 | 19,153 | 230.9 | 217.6 |
| control A | 2 | 66 | 90 | 1.38 | 5,659 | 16,101 | 187.9 | 184.7 |
| control A | 3 | 46 | 103 | 2.24 | 5,219 | 16,092 | 237.0 | 226.7 |
| control B | 1 | 46 | 94 | 2.09 | 6,432 | 17,725 | 228.3 | 223.6 |
| control B | 2 | 61 | 108 | 1.80 | 3,672 | 15,968 | 181.9 | 178.6 |
| control B | 3 | 57 | 101 | 1.77 | 5,289 | 15,669 | 213.5 | 210.1 |
| plugin default | 1 | 64 | 86 | 1.38 | 4,051 | 17,542 | – | 209.4 (`start_run` → `finish`) |
| plugin default | 2 | 44 | 84 | 1.98 | 4,294 | 17,757 | – | 244.0 |
| plugin default | 3 | 76 | 99 | 1.33 | 5,871 | 21,683 | – | 274.7 |
| plugin isolated | 1 | 54 | 97 | 1.85 | 6,001 | 21,616 | – | 223.8 |
| plugin isolated | 2 | 79 | 109 | 1.41 | 6,447 | 23,784 | – | 259.2 |
| plugin isolated | 3 | 41 | 94 | 2.38 | 4,364 | 19,147 | – | 246.6 |

| group | model turns | tool calls per turn | thinking tokens | output tokens |
|---|---|---|---|---|
| POC 23 Sep | 18–22 | 3.76–4.11 | 801–1,344 | 8,629–10,275 |
| control A | 46–66 | 1.38–2.24 | 5,219–7,363 | 16,092–19,153 |
| control B | 46–61 | 1.77–2.09 | 3,672–6,432 | 15,669–17,725 |
| plugin default | 44–76 | 1.33–1.98 | 4,051–5,871 | 17,542–21,683 |
| plugin isolated | 41–79 | 1.41–2.38 | 4,364–6,447 | 19,147–23,784 |

Definitions (the same as `project/05.4-runtime-diff.md` § 3 and § Experiment A, whose plugin and 23 Sep figures are reused here):
- **Model turns:** API calls. For the POC, CLI `status: requesting` events in `transcript.jsonl`; for the plugin, distinct `message.id`.
- **Tool calls:** the budget counter (`budget_used.tool_calls`; plugin: the trajectory's budget count, without `start_run`).
- **Tool calls per turn:** copied from 05.4's convention so the 23 Sep and plugin figures are unchanged:
  - for the POC (23 Sep and control), tool calls ÷ the manifest's `budget_used.turns`, which is one less than the API calls in most runs;
  - for the plugin, tool calls including `start_run` ÷ (API calls − 1).
  - Dividing by API calls instead gives the same picture: POC 23 Sep 3.59–4.11, control 1.36–2.24.
- **Thinking tokens:** `model_usage["claude-sonnet-5"].thinkingTokens` (plugin: `modelUsage.thinkingTokens`).
- **Output tokens:** POC: the manifest's `tokens.output_tokens`, the sum of `manifest.turns`. In A3 and B3 it is 8 and 2 above `model_usage.outputTokens` (16,084, 15,667). Plugin: `modelUsage.outputTokens`.
- **Duration:**
  - The harness session time (`manifest.duration_s`) exists only for the POC.
  - The plugin's figure runs from `start_run` to `finish` in the trajectory.
  - The last column gives the nearest POC equivalent, from the first trajectory row to `finish`.

Other per-run figures for the control runs:

| run | screenshots | findings | SDK `num_turns` | cost $ (notional) |
|---|---|---|---|---|
| A1 | 7 | 18 | 100 | 0.752 |
| A2 | 4 | 15 | 92 | 0.626 |
| A3 | 5 | 16 | 105 | 0.592 |
| B1 | 6 | 16 | 96 | 0.618 |
| B2 | 5 | 17 | 110 | 0.666 |
| B3 | 4 | 15 | 103 | 0.615 |

The 23 Sep runs took 2–4 screenshots and reported 20, 19 and 19 findings. In each run, one of them was on known issue U03.

## 4. Statements

**(a) The 23 Sep POC result does not reproduce today.** Recorded code and versions are identical:
- the code at `1b6b61a` (control A);
- prompt and harness SHA-256;
- `claude-agent-sdk` 0.2.158 and CLI 2.1.280;
- `model_pinned` and `model_reported` `claude-sonnet-5`;
- the whole SDK init block.

The served model snapshot is not recorded in any of these runs, and the 23 Sep Python and Playwright versions are inferred, not recorded (`05.5` § 6).
- **Recall:** 23 Sep 18–19 (mean 18.3), control A 15–18 (mean 16.3). One of six control runs (A1, 18) reaches the 23 Sep minimum.
- **D10:** found in 3 of 3 runs on 23 Sep and 0 of 6 control runs. It was examined but not reported in each control run.
- **Behaviour:** model turns 18–22 → 46–66, tool calls per turn 3.76–4.11 → 1.38–2.24, thinking tokens 801–1,344 → 3,672–7,363, output tokens 8,629–10,275 → 15,669–19,153. None of these ranges overlap.

**(b) Control A and B do not differ in recall.** A scored 15–18 (mean 16.3) and B 15–17 (mean 16.0), and their behaviour ranges overlap.
- **Per defect:** G03 was found 3/3 in A and 0/3 in B, and A06 3/3 vs 1/3. G01 (2/3 vs 3/3), G02 (1/3 vs 2/3), A03 (0/3 vs 1/3) and D07 (0/3 vs 1/3) differ by one run each. D04 is 1/3 in both, and D10 is 0/3 in both.
- The one model-visible difference between A and B (05.5 § 7, an error-message path) was not hit in any run. With three runs per group, the per-defect splits are not attributed to the code difference.

**(c) The plugin and today's POC cannot be told apart by recall or by the turn and thinking measures.**
- **Recall:** today's POC runs scored 15–18 (mean 16.2 over six runs). Plugin default scored 15–17 and isolated 14–16, so the ranges overlap.
- **Behaviour:** today's POC ranges overlap the plugin's on every measure:
  - model turns: 46–66 vs 41–79;
  - tool calls per turn: 1.38–2.24 vs 1.33–2.38;
  - thinking tokens: 3,672–7,363 vs 4,051–6,447.
  - Output tokens are lower for today's POC: 15,669–19,153 vs 17,542–23,784.
- **D10:** missed in all 12 runs across today's POC and the plugin, examined but not reported each time.
- **G03:** today's POC found it in 3 of 6 runs, the plugin in 1 of 6.
- **A03:** today's POC found it in 1 of 6 runs, the plugin in 2 of 6.
