# Experiment A: isolated plugin runs vs default plugin runs vs POC explorer

Experiment A ran plugin 0.1.0 unchanged, from a neutral temp folder outside any git repository, with `--setting-sources ""` and `--effort high`.
The setup and acceptance checks are in `project/05.4-runtime-diff.md` § Experiment A.
This file compares those three runs ("isolated") with the three default plugin runs and the POC explorer runs 1, 2 and 4.
The default-vs-POC comparison it builds on is `../20260928-plugin-v0.1.0/comparison.md`, left unchanged.

Inputs (all status `completed`):

| group | run | source folder under `../i18n-explorer/i18n-explorer-runs/` | report |
|---|---|---|---|
| isolated | 1 | `20260929-150018-localhost-5002` | `run-1/` |
| isolated | 2 | `20260929-150903-localhost-5002` | `run-2/` |
| isolated | 3 | `20260929-151354-localhost-5002` | `run-3/` |
| isolated | 1–3 together | | `seeded-stability/` |
| default | 1, 2, 3 | `20260928-161518`, `20260929-125402`, `20260929-125842` (`-localhost-5002`) | `../20260928-plugin-v0.1.0/seeded/`, `seeded-run-2/`, `seeded-run-3/` |
| POC | 1, 2, 4 | `../i18n-qa/artifacts/20260923-v2/seeded/findings-ai-explorer-{1,2,4}.json` | scored with `scoring.matcher.score_run` |

Each isolated `findings.json` was converted with `scoring.adapters.plugin_v1` and scored with `scoring.score --build seeded`.
The stability report scores copies of the three converted files together, the same way as the default and POC stability reports.
The source files' SHA-256 checksums matched before and after conversion.

**Element notation in isolated run 3.** This run writes `element` as `testid=X`, without brackets, a third form after the bare testid and `[testid=X]`.
With the adapter as it was, every run 3 finding had a null testid and was matched on text alone. The run scored 13/21, and its rate-note finding matched control C07 as a false positive.
Since commit `03b5b7e`, the adapter takes X from `testid=X` under the same rule as `[testid=X]`: only when it is the only testid in `element`.
Re-converting the six other plugin runs (three default seeded, the clean run, isolated runs 1 and 2) gives byte-identical output.
With the change, run 3 scores 14/21 with no false positive. All run 3 figures below use the corrected conversion.

## 1. Per-defect detection (seeded build)

| id | category | POC 1 | POC 2 | POC 4 | default 1 | default 2 | default 3 | isolated 1 | isolated 2 | isolated 3 | POC | default | isolated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D02 | placeholder | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D04 | truncation | no | no | no | no | no | yes | yes | no | no | 0/3 | 1/3 | 1/3 |
| D05 | number_currency_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D06 | date_format | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D07 | lang_attribute | no | no | no | no | no | no | no | no | no | 0/3 | 0/3 | 0/3 |
| D08 | locale_navigation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| D10 | plural | yes | yes | yes | no | no | no | no | no | no | 3/3 | 0/3 | 0/3 |
| G01 | terminology | yes | no | no | no | no | no | yes | yes | no | 1/3 | 0/3 | 2/3 |
| G02 | terminology | yes | yes | yes | yes | yes | yes | no | yes | no | 3/3 | 3/3 | 1/3 |
| G03 | terminology | yes | yes | yes | no | no | yes | no | no | no | 3/3 | 1/3 | 0/3 |
| G04 | register | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| A01 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| A02 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| A03 | mistranslation | yes | yes | yes | yes | yes | no | no | no | no | 3/3 | 2/3 | 0/3 |
| A04 | mistranslation | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| A05 | omission | yes | yes | yes | yes | yes | yes | yes | yes | yes | 3/3 | 3/3 | 3/3 |
| A06 | image_text | yes | yes | yes | no | yes | yes | yes | yes | yes | 3/3 | 2/3 | 3/3 |
| A07 | image_text | yes | yes | yes | yes | no | yes | yes | yes | yes | 3/3 | 2/3 | 3/3 |
| **total** | | **19** | **18** | **18** | **15** | **15** | **17** | **16** | **16** | **14** | | | |

### Recall per run

| group | run 1 | run 2 | third run (POC 4, plugin 3) | range | mean |
|---|---|---|---|---|---|
| POC | 19 (0.905) | 18 (0.857) | 18 (0.857) | 18–19 | 18.3 (0.873) |
| plugin default | 15 (0.714) | 15 (0.714) | 17 (0.810) | 15–17 | 15.7 (0.746) |
| plugin isolated | 16 (0.762) | 16 (0.762) | 14 (0.667) | 14–16 | 15.3 (0.730) |

- The isolated range (14–16) overlaps the default range (15–17) and does not reach the POC range (18–19).
- Across all six plugin runs, recall ranges from 14 to 17. Every plugin run is below the worst POC run.

### Found in every run, some runs, none

| group | every run | some runs | no run |
|---|---|---|---|
| POC | 18 | 1: G01 | 2: D04, D07 |
| plugin default | 13 | 5: A03, A06, A07 (2/3); D04, G03 (1/3) | 3: D07, D10, G01 |
| plugin isolated | 14: D01, D02, D03, D05, D06, D08, D09, G04, A01, A02, A04, A05, A06, A07 | 3: G01 (2/3); D04, G02 (1/3) | 4: D07, D10, G03, A03 |

Per defect, isolated compared with default:

- **More often found:** G01 (0/3 → 2/3), A06 and A07 (2/3 → 3/3).
- **Less often found:** G02 (3/3 → 1/3), A03 (2/3 → 0/3) and G03 (1/3 → 0/3).
- **Unchanged:** the other 15, including D10 (0/3 in both groups).

Seeded precision is 1.000 in all three isolated runs: no control false positives and no unclassified findings.
Isolated run 2 also reported the amount-input issue on `/fr/apply` (`apply-amount-input`), which matches known issue U05. The default seeded runs did not report it.

## 2. Defects the default plugin kept missing

These are D10 and G03, plus every defect missed in at least 2 of 3 default runs: D04, D07 and G01.

| id | isolated 1 | isolated 2 | isolated 3 |
|---|---|---|---|
| D10 | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported |
| G03 | missed: examined but not reported | missed: examined but not reported | missed: examined but not reported |
| G01 | found | found | missed: examined but not reported |
| D04 | found | missed: reached but not examined | missed: reached but not examined |
| D07 | missed: reached but not examined | missed: reached but not examined | missed: reached but not examined |

Method, from each isolated run's `trajectory.jsonl` (the same as in the default comparison):

- **Reached:** a row whose `path` is the defect's French page.
- **Examined:** a `read_page`, `inspect` or `page_info` call on that page whose `result` shows the defect.
  - For text defects, that means the result contains the seeded text.
  - For D07, it means a `page_info` result on the page, since `read_page` does not print the document language.
  - For D04, it means an `inspect` result on `apply-submit-button` showing the overflow.
  - For every row cited, `result_chars` equals the length of the stored `result`.
- **Screenshots** are listed but not counted as evidence, since they can't be searched.

Evidence:

| id | page | run | reached (seq) | examining call | screenshots of the page | report_finding on the element |
|---|---|---|---|---|---|---|
| D10 | `/fr/dashboard` | 1 | 36, 37, 68, 69 | seq 37 `read_page`: `span "0 prêts actifs" [testid=dashboard-active-loans-count]` | none | none |
| D10 | `/fr/dashboard` | 2 | 50, 51, 58–60, 81, 82 | seq 51 `read_page`: same line | none | none |
| D10 | `/fr/dashboard` | 3 | 45, 46 | seq 46 `read_page`: same line | none | none |
| G03 | `/fr/` | 1 | 0–2, 84, 85 | seq 1 `read_page`: `link "Appliquer pour un prêt" [testid=landing-cta-apply] -> /fr/apply` | seq 85 | none |
| G03 | `/fr/` | 2 | 0–2, 99, 100 | seq 1 `read_page`: same line | seq 100 | none |
| G03 | `/fr/` | 3 | 0–2, 5, 6, 75 | seq 1 `read_page`: same line | seq 6 | none |
| G01 | `/fr/apply` | 1 | 6–80 (30 rows) | seq 7, 9, 18, 78 `read_page` | seq 79 | seq 96 (found) |
| G01 | `/fr/apply` | 2 | 6–95 (31 rows) | seq 7, 9, 18, 94 `read_page` | seq 86 | seq 104 (found) |
| G01 | `/fr/apply` | 3 | 9–81 (23 rows) | seq 10, 12, 21 `read_page`: `label "Adresse e-mail" [testid=apply-email-label]` | none | none |
| D04 | `/fr/apply` | 1 | 6–80 (30 rows) | seq 80 `inspect apply-submit-button`: `scrollWidth 290 / clientWidth 210` | seq 79 | seq 83 (found) |
| D04 | `/fr/apply` | 2 | 6–95 (31 rows) | none: no `inspect` of the button | seq 86 | none |
| D04 | `/fr/apply` | 3 | 9–81 (23 rows) | none: its one `inspect` of `apply-submit-button` (seq 91) was made on `/fr/calculator` and returned "no match" | none | none |
| D07 | `/fr/application/AP-100482` | 1 | 31, 32 | none: `page_info` only on `/fr/` and `/fr/calculator` | none | none |
| D07 | `/fr/application/AP-100482` | 2 | 23, 24, 96, 98 | none: `page_info` only on `/fr/`, `/fr/apply` and `/fr/dashboard` | none | none |
| D07 | `/fr/application/AP-100482` | 3 | 33, 34, 82, 83 | none: `page_info` only on `/fr/` and `/fr/apply` | seq 83 | none |

- For D07, the trajectory's server-side `lang` field is `en` on every row for that page, in all three runs. That field is logged by the server, not returned to the agent.
- The G01 findings in isolated runs 1 and 2 name two testids (`apply-email-label / apply-error-email`), so they matched on text ("Adresse e-mail").

Isolated runs also miss two defects that the default runs mostly found:

- **A03:** missed in all 3 isolated runs. It was examined but not reported in each: `link "Déclaration mensuelle"` appears in `read_page` at seq 37, 51 and 46.
- **G02:** missed in isolated runs 1 and 3. It was examined but not reported in both: `read_page` at seq 37 and 46.

In both cases the text is in the same `/fr/dashboard` `read_page` result as D10.

## 3. Plural rule (French zero takes the singular)

The correct French text is "0 prêt actif" (CLDR/Babel: `Locale.parse('fr_CA').plural_form(0) == 'one'`). The seeded build shows "0 prêts actifs" (D10).

| run | text read on `/fr/dashboard` | reported | handled correctly? |
|---|---|---|---|
| isolated 1 | "0 prêts actifs" (seq 37) | no | no |
| isolated 2 | "0 prêts actifs" (seq 51) | no | no |
| isolated 3 | "0 prêts actifs" (seq 46) | no | no |

- In each run, the agent read `/en/dashboard` two calls later ("0 active loans": seq 39, 53, 48).
- No `report_finding` call and no finish summary mentions "plural", "pluriel", "singular", "prêt actif" or "active loans".
- The trajectory records tool calls, not the agent's reasoning.

With the three default runs, the plugin has now missed the plural error in 6 of 6 seeded runs. The POC reported it in 3 of 3.

## 4. Per-run activity

Same method as the default comparison: all figures come from each run's `trajectory.jsonl`, and duration runs from `start_run` to `finish`.

| run | tool calls (budget) | report_finding | exploration calls | screenshots | duration (s) | findings | fr pages | en pages |
|---|---|---|---|---|---|---|---|---|
| default 1 | 86 | 15 | 70 | 4 | 209.4 | 15 | 5/5 | 5/5 |
| default 2 | 84 | 15 | 68 | 3 | 244.0 | 15 | 5/5 | 5/5 |
| default 3 | 99 | 17 | 81 | 5 | 274.7 | 17 | 5/5 | 5/5 |
| isolated 1 | 97 | 16 | 80 | 6 | 223.8 | 16 | 5/5 | 5/5 |
| isolated 2 | 109 | 17 | 91 | 6 | 259.2 | 17 | 5/5 | 5/5 |
| isolated 3 | 94 | 14 | 79 | 6 | 246.6 | 14 | 5/5 | 5/5 |

The POC seeded runs made 74–79 tool calls (54–58 exploration calls), took 2–4 screenshots and ran 90.5–126.0 s of harness session time. Their figures are in the default comparison.

Tool errors:

- isolated 1: seq 95 `inspect` (no match for `dashboard-statement-link` on `/fr/calculator`);
- isolated 2: seq 41 `click`;
- isolated 3: seq 91 `inspect` (no match for `apply-submit-button` on `/fr/calculator`).
