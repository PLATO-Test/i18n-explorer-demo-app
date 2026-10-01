# Sonnet 5.5: POC explorer and plugin vs earlier groups

Three seeded runs of the POC explorer, three of plugin 0.1.0 at effort medium and three of plugin 0.1.0 at effort high, all on `claude-sonnet-5-5` (2026-10-01).
Run setup: `project/05.6-sonnet55-poc.md` and `project/05.6-sonnet55-plugin.md` (effort high: its section "Effort high").
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
| plugin S5.5 high | 1 | `…/20261001-134037-localhost-5002/findings.json` | completed; CLI `success` | `model_configured` `claude-sonnet-5-5`; 96 of 96 subagent assistant entries on it, all with `"effort":"high","perTurnEffort":"high"` | `plugin-high-run-1/` |
| plugin S5.5 high | 2 | `…/20261001-134259-localhost-5002/findings.json` | completed; CLI `success` | same; 104 of 104 | `plugin-high-run-2/` |
| plugin S5.5 high | 3 | `…/20261001-134521-localhost-5002/findings.json` | completed; CLI `success` | same; 108 of 108 | `plugin-high-run-3/` |
| plugin S5.5 high | 1–3 together | the three converted files | | | `plugin-high-stability/` |

- `20261001-125414-failed-attempt` was not scored: no model turn ran (05.6-plugin § 4).
- POC `model_usage` lists `claude-haiku-4-5-20251001` next to `claude-sonnet-5-5` in every run: 929 input and 15 output tokens, the same in each. The 23 Sep and control A manifests list Haiku the same way. The plugin's `modelUsage` lists only `claude-sonnet-5-5`.
- The POC files were scored with `scoring.score --build seeded`, as in phase 3.
- The plugin files were converted with `scoring.adapters.plugin_v1` (output kept as `plugin-run-N/findings.converted.json`), then scored the same way.
- The stability reports score each group's three files together.
- The six source files' SHA-256 matched 05.6 before scoring and were unchanged after. The same holds for the three effort-high files, scored the same way as the medium ones.
- The earlier groups come from `../20260929-poc-control/A-run-1..3/` and `../20260928-plugin-v0.1.0/seeded/`, `seeded-run-2/`, `seeded-run-3/`.
- The 23 Sep runs were re-scored outside the repo, with the same command. The totals (19, 18, 18) and per-defect results match `../20260929-poc-control/comparison.md`.

**Code baselines.** The POC S5.5 runs used a worktree of `0663db9`, the control B commit, with only `MODEL` changed (05.6-poc § 3). Control A ran at `1b6b61a`.
- Control A is in the tables, as requested.
- Control B (`0663db9`, Sonnet 5) is the code-identical baseline. It is given in the recall table and in § 6.

## 1. Per-defect detection (seeded build)

"POC 23" is the 23 Sep POC runs 1, 2 and 4. "A" is POC control A. "def" is plugin default. "P55" is POC S5.5, "G55" is plugin S5.5 at effort medium and "G5H" is plugin S5.5 at effort high.

| id | category | POC 23 1 | POC 23 2 | POC 23 4 | A 1 | A 2 | A 3 | def 1 | def 2 | def 3 | P55 1 | P55 2 | P55 3 | G55 1 | G55 2 | G55 3 | G5H 1 | G5H 2 | G5H 3 | POC 23 | A | def | P55 | G55 | G5H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D02 | placeholder | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D04 | truncation | no | no | no | yes | no | no | no | no | yes | no | no | no | no | no | no | yes† | no | no | 0/3 | 1/3 | 1/3 | 0/3 | 0/3 | 1/3† |
| D05 | number_currency_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D06 | date_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D07 | lang_attribute | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| D08 | locale_navigation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| D10 | plural | yes | yes | yes | no | no | no | no | no | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| G01 | terminology | yes | no | no | yes | no | yes | no | no | no | yes | yes | yes | no | yes | no | yes | yes | yes | 1/3 | 2/3 | 0/3 | 3/3 | 1/3 | 3/3 |
| G02 | terminology | yes | yes | yes | yes | no | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| G03 | terminology | yes | yes | yes | yes | yes | yes | no | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| G04 | register | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A01 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A02 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A03 | mistranslation | yes | yes | yes | no | no | no | yes | yes | no | yes | yes | yes | no | no | yes | yes | yes | yes | 3/3 | 0/3 | 2/3 | 3/3 | 1/3 | 3/3 |
| A04 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A05 | omission | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| A06 | image_text | yes | yes | yes | yes | yes | yes | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| A07 | image_text | yes | yes | yes | yes | yes | yes | yes | no | yes | yes | yes | yes | no | no | yes | yes | yes | yes | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 |
| **total** | | **19** | **18** | **18** | **18** | **15** | **16** | **15** | **15** | **17** | **19** | **19** | **19** | **16** | **17** | **18** | **20**† | **19** | **19** | | | | | | |

† **D04 in G5H 1** is the scorer's result, but the finding it credits is not about truncation.
- The finding (report_finding seq 24) has category `terminology` and no testid (element `button "Soumettre ma demande de prêt"`). Its `fr_text` is "Soumettre ma demande de prêt", its fix "Soumettre la demande", and its description: `Minor: adds "de prêt" and a possessive not in English; acceptable but differs. (Low confidence.)`
- The scorer matched it by text containment. D04's `fr_seeded` and `fr_clean` are both "Soumettre ma demande de prêt", so the same wording is on the clean build. The report marks the category as not correct.
- The run took no screenshot of `/fr/apply`. No finding and no `finish` summary mentions clipping, truncation or width.
- Without this credit, G5H 1 is 19, the same as G5H 2 and 3.

### Recall per run

| group | model | run 1 | run 2 | third run (POC 23 Sep: run 4) | range | mean |
|---|---|---|---|---|---|---|
| POC 23 Sep | Sonnet 5 | 19 (0.905) | 18 (0.857) | 18 (0.857) | 18–19 | 18.3 (0.873) |
| POC control A (`1b6b61a`) | Sonnet 5 | 18 (0.857) | 15 (0.714) | 16 (0.762) | 15–18 | 16.3 (0.778) |
| POC control B (`0663db9`), for reference | Sonnet 5 | 16 (0.762) | 17 (0.810) | 15 (0.714) | 15–17 | 16.0 (0.762) |
| plugin default | Sonnet 5 | 15 (0.714) | 15 (0.714) | 17 (0.810) | 15–17 | 15.7 (0.746) |
| **POC S5.5** (`0663db9` + model) | Sonnet 5.5 | 19 (0.905) | 19 (0.905) | 19 (0.905) | 19–19 | 19.0 (0.905) |
| **plugin S5.5, effort medium** | Sonnet 5.5 | 16 (0.762) | 17 (0.810) | 18 (0.857) | 16–18 | 17.0 (0.810) |
| **plugin S5.5, effort high** | Sonnet 5.5 | 20† (0.952) | 19 (0.905) | 19 (0.905) | 19–20 | 19.3 (0.921) |

† Includes the D04 credit above. Without it: 19 in every run, mean 19.0 (0.905).

### Found in every run, some runs, none

| group | every run | some runs | no run |
|---|---|---|---|
| POC S5.5 | 19 | none | 2: D04, D07 |
| plugin S5.5, effort medium | 16 | 3: G01, A03, A07 (1/3 each) | 2: D04, D07 |
| plugin S5.5, effort high | 19 | 1: D04 (1/3, †) | 1: D07 |

- POC S5.5 found the same 19 defects in all three runs.
- Plugin S5.5 at effort high found the same 19 in all three runs, plus the D04 credit in run 1. These 19 are the POC S5.5 set.
- D07 was missed in all nine S5.5 runs. D04 was missed in all of them apart from that credit. The 23 Sep POC also missed both in every run.

## 2. G01, A03, A07, D10, G03 and the zero-plural rule in the Sonnet 5.5 runs

| id | P55 1 | P55 2 | P55 3 | G55 1 | G55 2 | G55 3 | G5H 1 | G5H 2 | G5H 3 |
|---|---|---|---|---|---|---|---|---|---|
| G01 | found | found | found | missed: examined but not reported | found | missed: examined but not reported | found | found | found |
| A03 | found | found | found | missed: examined; named only in another finding's description | missed: examined but not reported | found | found | found | found |
| A07 | found | found | found | missed: reached; image element read; no screenshot of the page | missed: reached; image element read; one viewport screenshot, image cut off (see below) | found | found | found | found |
| D10 | found | found | found | found | found | found | found | found | found |
| G03 | found | found | found | found | found | found | found | found | found |
| zero-plural rule | handled | handled | handled | handled | handled | handled | handled | handled | handled |

The G01 and A07 rows were added with the effort-high group, and their G55 cells were classified with the same method. The POC runs found G01 and A07 in every run, so their trajectories are not listed below.

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
| D10 | `/fr/dashboard` | G5H 1 | 2, from seq 44 | seq 44 `read_page` | none | seq 49 |
| D10 | `/fr/dashboard` | G5H 2 | 2, from seq 45 | seq 45 `read_page` | none | seq 50 |
| D10 | `/fr/dashboard` | G5H 3 | 4, from seq 52 | seq 52 `read_page` | none | seq 57 |
| G03 | `/fr/` | G5H 1 | 4, from seq 0 | seq 1 `read_page` | none | seq 8 |
| G03 | `/fr/` | G5H 2 | 4, from seq 0 | seq 1 `read_page` | none | seq 9 |
| G03 | `/fr/` | G5H 3 | 6, from seq 0 | seq 1 `read_page` | seq 10 | seq 6 |
| A03 | `/fr/dashboard` | G5H 1 | 2, from seq 44 | seq 44 `read_page` | none | seq 51 |
| A03 | `/fr/dashboard` | G5H 2 | 2, from seq 45 | seq 45 `read_page` | none | seq 52 |
| A03 | `/fr/dashboard` | G5H 3 | 4, from seq 52 | seq 52 `read_page` | none | seq 56 |
| G01 | `/fr/apply` | G55 1 | 17, from seq 7 | seq 7, 9, 17 `read_page`: `label "Adresse e-mail" [testid=apply-email-label]` | none | none |
| G01 | `/fr/apply` | G55 2 | 18, from seq 10 | seq 10, 12, 19 `read_page` | none | seq 21 |
| G01 | `/fr/apply` | G55 3 | 17, from seq 10 | seq 10, 12, 19 `read_page`: same line | none | none |
| G01 | `/fr/apply` | G5H 1 | 17, from seq 10 | seq 10, 12, 18 `read_page` | none | seq 23 |
| G01 | `/fr/apply` | G5H 2 | 20, from seq 11 | seq 11, 13, 20 `read_page` | none | seq 22 |
| G01 | `/fr/apply` | G5H 3 | 19, from seq 12 | seq 12, 14, 22 `read_page` | none | seq 32 |

**A03 in G55 1.** The run had no finding on `dashboard-statement-link`.
- The seeded text appears only in the description of the G02 finding at seq 50, which has element `dashboard-balance-label`, `fr_text` "Balance du compte", and the description: `Anglicism "balance"; also "Déclaration mensuelle" should be "Relevé mensuel".`
- The scorer credits that finding to G02.
- The earlier comparisons' "reported" rule also counted a `report_finding` whose arguments contain the seeded text anywhere. Under that rule this case would have been counted as "reported", so it is labelled separately here.

**A03 in G55 2.** No `report_finding` call and no `finish` summary mentions "Déclaration", "statement" or "Relevé".

**G01 in G55 1 and G55 3.** No `report_finding` call and no `finish` summary mentions "e-mail", "email" or "courriel".

**A07.** The seeded text is only in the image's pixels. The alt text ("Taux variable : 5,2 %") is correct, so the text-based "examined" rule cannot apply. For A07 the table lists instead:
- the `read_page` calls on `/fr/calculator` whose result has the image element (`img "Taux variable : 5,2 %" [testid=calculator-promo-image] … src=/static/img/promo-c.png`);
- every screenshot of `/fr/calculator`, and whether it was full-page (the trajectory's `full_page`).

| page | run | reached (rows) | `read_page` with the image element | screenshots of the page | report_finding on the element |
|---|---|---|---|---|---|
| `/fr/calculator` | G55 1 | 4, from seq 29 | seq 29, 31 | none | none |
| `/fr/calculator` | G55 2 | 10, from seq 42 | seq 42, 48 | seq 54 (viewport) | none |
| `/fr/calculator` | G55 3 | 9, from seq 42 | seq 42, 51 | seq 56 (full page) | seq 57 |
| `/fr/calculator` | G5H 1 | 12, from seq 54 | seq 54, 64, 74 | seq 65 (full page) | seq 67 |
| `/fr/calculator` | G5H 2 | 17, from seq 55 | seq 55, 66, 77 | seq 60 (viewport), seq 72 (full page) | seq 73 |
| `/fr/calculator` | G5H 3 | 12, from seq 62 | seq 62, 73, 82 | seq 74 (full page) | seq 76 |

- Each of the four A07 reports came one or two rows after a full-page screenshot of `/fr/calculator` (56 → 57, 65 → 67, 72 → 73, 74 → 76). Each gives the image text as "Taux fixe : 4,9 %".
- Neither miss had a full-page screenshot of the page.
- G55 2's screenshot 054 was viewed by hand for this table, so this is a manual observation, not a searchable record. The calculator modal is open in it, and only the top edge of the promo image shows at the bottom, with no text.
- G55 2's `finish` summary says: "Not checked: the contents of the promo images".

**Zero-plural rule.** The correct French is "0 prêt actif". The seeded build shows "0 prêts actifs" (D10).

| run | "0 prêts actifs" read (seq) | `/en/dashboard` `read_page` (seq) | reported (seq) | `expected` / `suggested_fix` | description |
|---|---|---|---|---|---|
| P55 1 | 35 | 37 | 40 | "0 prêt actif" | "In French, zero takes the singular form." |
| P55 2 | 44 | 46 | 50 | "0 prêt actif" | same |
| P55 3 | 44 | 46 | 50 | "0 prêt actif" | "In French, zero takes the singular form; plural used for 0." |
| G55 1 | 45 | none | 49 | "0 prêt actif" | "In French, zero takes the singular." |
| G55 2 | 33 | 40 (after the report) | 35 | "0 prêt actif" | same |
| G55 3 | 32 | 39 (after the report) | 34 | "0 prêt actif" | same |
| G5H 1 | 44 | 46 | 49 | "0 prêt actif" | "In French, zero takes the singular; plural is used for 0." |
| G5H 2 | 45 | 47 | 50 | "0 prêt actif" | "In French, zero takes the singular; "0 prêts actifs" is plural." |
| G5H 3 | 52 | 54 | 57 | "0 prêt actif" | "In French, zero takes the singular form (0 and 1 are singular)." |

All nine runs state the rule and give the correct singular form.

## 3. Precision and findings that match no defect

| run | findings | matched a defect | control false positive | unclassified | known issue | precision |
|---|---|---|---|---|---|---|
| P55 1 | 22 | 19 | 1 (C01) | 0 | 2 (U03, U04) | 0.950 |
| P55 2 | 21 | 19 | 0 | 0 | 2 (U03, U06) | 1.000 |
| P55 3 | 20 | 19 | 0 | 0 | 1 (U03) | 1.000 |
| G55 1 | 16 | 16 | 0 | 0 | 0 | 1.000 |
| G55 2 | 17 | 17 | 0 | 0 | 0 | 1.000 |
| G55 3 | 18 | 18 | 0 | 0 | 0 | 1.000 |
| G5H 1 | 21 | 20† | 0 | 0 | 1 (U03) | 1.000 |
| G5H 2 | 20 | 19 | 0 | 0 | 1 (U03) | 1.000 |
| G5H 3 | 20 | 19 | 0 | 1 | 0 | 0.950 |

- Precision is matched ÷ (findings − known-issue findings).
- The scorer's `false_positive_count` adds control false positives and unclassified findings together, so it is 1 in P55 1 and G5H 3 and 0 in P55 2.
- † G5H 1's 20 includes the D04 credit from a wording finding (§ 1). Counted as a defect match, as the scorer does; as a non-match its precision would be 19 ÷ 20 = 0.950.
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
| G5H 1 | known issue U03 | `/fr/inexistant` | – | missing_translation / low | Not Found / The requested URL was not found on the server. | Localized 404 page: "Page introuvable". | 404 page under /fr/ is the generic English server error, without site header or French text. |
| G5H 2 | known issue U03 | `/fr/inexistant` | – (element `heading "Not Found"`) | missing_translation / low | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | Page introuvable. L'adresse demandée est introuvable sur le serveur. ... | 404 page under /fr/ is the untranslated default English error page without site header or French text. |
| G5H 3 | unclassified | `/fr/nonexistent` | – | lang_attribute / low | Not Found / The requested URL was not found on the server. | Localized fr-CA 404 page with lang="fr-CA" and a link back | 404 page under /fr/ is English with html lang="en" and no localized layout. |

G5H 3's 404 finding is unclassified because of its category.
- It reports the same page as the U03 hits in G5H 1 and 2, but with category `lang_attribute`. U03 lists only `missing_translation`, `hardcoded_text` and `other`.
- D07 (`lang_attribute`) is on the summary page, not `/fr/nonexistent`, so it does not match either.
- `known_issues.yaml` was not changed.

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
| **plugin S5.5 high** | 1 | high | 24 | – | 78 | 3.43 | 670 | 13,503 | – | 112.9 (`start_run` → `finish`) |
| **plugin S5.5 high** | 2 | high | 23 | – | 83 | 3.82 | 996 | 13,869 | – | 115.5 |
| **plugin S5.5 high** | 3 | high | 22 | – | 91 | 4.38 | 897 | 14,613 | – | 138.6 |

| group | model turns | tool calls per turn | thinking tokens | output tokens | duration, first tool call → `finish` (s) |
|---|---|---|---|---|---|
| POC 23 Sep | 18–22 | 3.76–4.11 | 801–1,344 | 8,629–10,275 | 86.8–101.8 |
| POC control A | 46–66 | 1.38–2.24 | 5,219–7,363 | 16,092–19,153 | 184.7–226.7 |
| POC control B | 46–61 | 1.77–2.09 | 3,672–6,432 | 15,669–17,725 | 178.6–223.6 |
| plugin default | 44–76 | 1.33–1.98 | 4,051–5,871 | 17,542–21,683 | 209.4–274.7 |
| POC S5.5 | 21–23 | 3.48–3.75 | 872–1,047 | 9,432–10,001 | 78.0–102.9 |
| plugin S5.5, medium | 16–17 | 3.25–3.73 | 462–494 | 8,844–10,659 | 71.8–81.0 |
| plugin S5.5, high | 22–24 | 3.43–4.38 | 670–996 | 13,503–14,613 | 112.9–138.6 |

Screenshots taken (budget count): plugin S5.5 medium 2 / 1 / 1, high 4 / 5 / 3.

**Effort.**
- **Plugin S5.5:** every explorer assistant entry carries `"effort":"medium","perTurnEffort":"medium"` (05.6-plugin § 5).
- **Plugin S5.5 high:** every explorer assistant entry carries `"effort":"high","perTurnEffort":"high"` (05.6-plugin, "Effort high").
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
  - Plugin: tool calls including `start_run` ÷ (API calls − 1). This gives 3.25 / 3.73 / 3.69 at medium and 3.43 / 3.82 / 4.38 at high.
  - 05.6-plugin divides by API calls instead (medium 3.06 / 3.50 / 3.47, high 3.29 / 3.65 / 4.18).
- **Thinking tokens:** `model_usage[<agent model>].thinkingTokens` (plugin: `modelUsage`).
- **Output tokens:** POC: the manifest's `tokens.output_tokens`. In P55 2 it is 3 above `result_usage.output_tokens` (9,429). Plugin: `modelUsage.outputTokens`.
- **Duration:** POC: `manifest.duration_s` and first trajectory row → `finish`. Plugin: `start_run` → `finish` in the trajectory, which equals the run's `duration_s`. The CLI's `duration_ms` was 80.3 / 78.3 / 88.0 s at medium and 120.1 / 123.3 / 145.2 s at high.

Other recorded differences for the plugin, Sonnet 5 default → Sonnet 5.5:
- Claude Code CLI 2.1.284 → 2.1.286.
- `maxOutputTokens` 64,000 → 128,000.
- The plugin was loaded from the repo's install → `--plugin-dir` on a temporary copy of tag `v0.1.0`.

Plugin S5.5, effort medium → effort high (05.6-plugin, "Effort high"):
- **Change to the plugin copy:** only the added `effort: high` line in `agents/explorer.md`. Model, `MODEL_CONFIGURED`, the command and `--plugin-dir` loading are the same.
- **Same in both groups:** CLI 2.1.286, `maxOutputTokens` 128,000, main session model `claude-opus-5-5`.
- **Recorded differences outside the copy:**
  - The built-in plugins listed at init: cc-plugin-diff (high run 1) and cc-plugin-plugin-authoring (high runs 2 and 3) were present only in the high runs.
  - The shared venv was re-synced to the new copy before high run 1.
  - The high runs started about 45 minutes after the medium runs (17:40–17:47 vs 16:56–17:01 UTC).

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

**(b) POC vs plugin (effort medium) on Sonnet 5.5.**
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

**(c) Plugin on Sonnet 5.5, effort high vs effort medium.**
- **Recall:** high 20†, 19, 19 (range 19–20, mean 19.3) vs medium 16, 17, 18 (range 16–18, mean 17.0). The ranges do not overlap.
  - † Without the D04 credit from a wording finding (§ 1), high is 19 in every run.
- **Per defect:** G01, A03 and A07 were found in 3/3 high runs vs 1/3 medium runs each. D04 was credited in 1/3 high runs (†) vs 0/3. The other 17 defects are equal.
  - Both found D10 and G03 in 3/3, both handled the zero-plural rule in 3/3, and both missed D07 in 3/3.
  - The medium misses of G01 and A03 were all on French pages whose `read_page` result had the seeded text (§ 2).
  - Each A07 report, in both groups, came one or two rows after a full-page screenshot of `/fr/calculator`. Neither medium miss had one.
- **Precision:** high 1.000, 1.000, 0.950 vs medium 1.000 in all three runs.
  - High run 3's 0.950 comes from one unclassified finding: the English 404 page, reported as `lang_attribute`.
  - High runs 1 and 2 reported the same page as `missing_translation`, which was credited to U03. The medium runs did not report it.
- **Behaviour:** these ranges do not overlap:
  - model turns 22–24 vs 16–17;
  - tool calls 78–91 vs 51–58;
  - thinking tokens 670–996 vs 462–494;
  - output tokens 13,503–14,613 vs 8,844–10,659;
  - duration 112.9–138.6 s vs 71.8–81.0 s;
  - screenshots 3–5 vs 1–2.
  - Tool calls per turn overlap (3.43–4.38 vs 3.25–3.73).
- **Setup:** the only change to the plugin copy was `effort: high`. The recorded differences outside the copy are listed in § 4.
- Each group has three runs. The data shows that recall and these behaviour figures differ between the groups. It does not show which behaviour difference, if any, produced the recall difference.

**(d) Plugin effort high vs POC on Sonnet 5.5.**
- **Recall:** plugin high 20†, 19, 19 vs POC 19, 19, 19.
  - Without the D04 credit the two groups are equal: 19 in every run.
- **Per defect:** both found the same 19 defects in every run, and both missed D07 in every run.
  - The only difference is D04: the POC missed it in every run, and plugin high run 1 was credited with it from a wording finding (†).
  - Both groups handled the zero-plural rule in every run.
- **Precision:** plugin high 1.000, 1.000, 0.950 vs POC 0.950, 1.000, 1.000.
  - Each group has one run below 1.000: POC run 1 from a control false positive (C01), plugin high run 3 from an unclassified 404 finding.
  - Known-issue hits: POC U03 in every run, plus U04 and U06 once each. Plugin high: U03 in runs 1 and 2.
- **Behaviour:**
  - These overlap: model turns (22–24 vs 21–23), tool calls (78–91 vs 75–80), tool calls per turn (3.43–4.38 vs 3.48–3.75) and thinking tokens (670–996 vs 872–1,047).
  - These do not overlap: output tokens (13,503–14,613 vs 9,432–10,001) and duration (112.9–138.6 s vs 78.0–102.9 s). The two durations are measured slightly differently (§ 4 definitions).
- **Effort:** the plugin recorded effort high. The POC sets no effort and records no level, so whether the two ran at the same effort level cannot be told from this data.
- **Other setup differences:** prompt, tools and runtime differ (05.4). The CLI is 2.1.280 for the POC and 2.1.286 for the plugin.
- None of the differences above is attributed to a cause.

## 6. Notes

- `project/05.6-sonnet55-poc.md` reports `costBasis: "unknown"` and `contextWindow: 200000` for `claude-sonnet-5-5` in the POC. The plugin's CLI (2.1.286) reports `costBasis: "list"` and `contextWindow: 1000000`. Neither figure is used here.
- The POC S5.5 runs each have one U03 hit, as the 23 Sep runs did. Control A had none.
- Plugin S5.5 high runs 1 and 2 each have one U03 hit. Run 3 reported the same page under a category U03 does not list (§ 3). Plugin S5.5 medium had no 404 finding.
