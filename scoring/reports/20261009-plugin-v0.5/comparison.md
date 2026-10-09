# i18n-explorer 0.5.x: default and quick presets

Six seeded runs per preset (three on plugin 0.5.0, 8 Oct; three on 0.5.1, 9 Oct) and one clean run per preset (0.5.1, 9 Oct), all on `claude-sonnet-5-5`.
Run setup, commands and SHA-256 of every source file: `project/05.10-i18n-explorer-v0.5-measurement.md`.
0.5.0 and 0.5.1 have the same agent and server code (0.5.1 changed only docs and the sample report), so the 8 Oct and 9 Oct runs of a preset are treated as one group of six. Folder names keep the date.

## Inputs

Source paths are relative to `C:\Users\AlexHotvianskyi\AppData\Local\Temp\i18n-measure\`. Status, plugin version and observed model/effort are from each findings.json's `run` block (`run.status`, `run.plugin_version`, `run.observed.models`, `run.observed.effort_levels`; the count is API responses per model / effort level).

| preset | build | run | source | date | plugin | status | model observed | effort observed | report |
|---|---|---|---|---|---|---|---|---|---|
| default | seeded | 1 | `default-1\i18n-explorer-runs\20261008-164125-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (20) | high (20) | `default-20261008-run-1/` |
| default | seeded | 2 | `default-2\i18n-explorer-runs\20261008-164500-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (19) | high (19) | `default-20261008-run-2/` |
| default | seeded | 3 | `default-3\i18n-explorer-runs\20261008-164916-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (20) | high (20) | `default-20261008-run-3/` |
| default | seeded | 1 | `v051-A-default-1\i18n-explorer-runs\20261009-092740-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (23) | high (23) | `default-20261009-run-1/` |
| default | seeded | 2 | `v051-A-default-2\i18n-explorer-runs\20261009-093012-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (19) | high (19) | `default-20261009-run-2/` |
| default | seeded | 3 | `v051-A-default-3\i18n-explorer-runs\20261009-093216-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (21) | high (21) | `default-20261009-run-3/` |
| default | seeded | all six | the six converted files | | | | | | `default-stability/` |
| quick | seeded | 1 | `quick-1\i18n-explorer-runs\20261008-164325-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (16) | medium (16) | `quick-20261008-run-1/` |
| quick | seeded | 2 | `quick-2\i18n-explorer-runs\20261008-164745-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (13) | medium (13) | `quick-20261008-run-2/` |
| quick | seeded | 3 | `quick-3\i18n-explorer-runs\20261008-165205-localhost-5002\findings.json` | 2026-10-08 | 0.5.0 | completed | claude-sonnet-5-5 (13) | medium (13) | `quick-20261008-run-3/` |
| quick | seeded | 1 | `v051-B-quick-1\i18n-explorer-runs\20261009-093437-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (13) | medium (13) | `quick-20261009-run-1/` |
| quick | seeded | 2 | `v051-B-quick-2\i18n-explorer-runs\20261009-093606-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (15) | medium (15) | `quick-20261009-run-2/` |
| quick | seeded | 3 | `v051-B-quick-3\i18n-explorer-runs\20261009-093733-localhost-5002\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (14) | medium (14) | `quick-20261009-run-3/` |
| quick | seeded | all six | the six converted files | | | | | | `quick-stability/` |
| default | clean | 1 | `v051-C-default\i18n-explorer-runs\20261009-093920-localhost-5001\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (19) | high (19) | `clean-default/` |
| quick | clean | 1 | `v051-C-quick\i18n-explorer-runs\20261009-094056-localhost-5001\findings.json` | 2026-10-09 | 0.5.1 | completed | claude-sonnet-5-5 (10) | medium (10) | `clean-quick/` |

- Each file was converted with `scoring.adapters.plugin_v1` (output kept as `<report>/findings.converted.json`) and scored with `scoring.score --build seeded` or `--build clean`.
- The stability reports score each preset's six `findings.converted.json` files together, copied into one folder outside the repo for the run.
- The 14 source files' SHA-256 matched 05.10 before scoring and were unchanged after.
- 8 Oct runs: which plugin commit was checked out, and whether the tree was clean, was not recorded (05.10).
- `quick-20261008-run-2`: the agent's closing reply says its `finish` summary claimed 17 findings; findings.json has 15 (05.10).
- The 8 Oct run folders also hold a `scored/` subfolder from an earlier session. It was not used. After scoring, its `findings.converted.json`, `report.json` and `report.md` were compared with the ones here: all three files are identical in all six runs.

## 1. Recall, precision and false positives per run (seeded build)

| preset | run | findings | matched a defect | known issue | control false positive | unclassified | recall | precision | false positives |
|---|---|---|---|---|---|---|---|---|---|
| default | `default-20261008-run-1` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 | 0 |
| default | `default-20261008-run-2` | 19 | 19 | 0 | 0 | 0 | 19/21 (0.905) | 1.000 | 0 |
| default | `default-20261008-run-3` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 | 0 |
| default | `default-20261009-run-1` | 20 | 19 | 1 (U03) | 0 | 0 | 19/21 (0.905) | 1.000 | 0 |
| default | `default-20261009-run-2` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 | 0 |
| default | `default-20261009-run-3` | 21 | 19 | 2 (U03, U04) | 0 | 0 | 19/21 (0.905) | 1.000 | 0 |
| quick | `quick-20261008-run-1` | 17 | 16 | 1 (U04) | 0 | 0 | 16/21 (0.762) | 1.000 | 0 |
| quick | `quick-20261008-run-2` | 15 | 14 | 1 (U04) | 0 | 0 | 14/21 (0.667) | 1.000 | 0 |
| quick | `quick-20261008-run-3` | 15 | 14 | 1 (U04) | 0 | 0 | 14/21 (0.667) | 1.000 | 0 |
| quick | `quick-20261009-run-1` | 16 | 15 | 1 (U04) | 0 | 0 | 15/21 (0.714) | 1.000 | 0 |
| quick | `quick-20261009-run-2` | 17 | 15 | 1 (U04) | 0 | 1 | 15/21 (0.714)† | 0.938† | 1† |
| quick | `quick-20261009-run-3` | 14 | 14 | 0 | 0 | 0 | 14/21 (0.667) | 1.000 | 0 |

| preset | recall min | recall max | recall median | precision min | precision max | precision median | false positives min | false positives max | false positives median |
|---|---|---|---|---|---|---|---|---|---|
| default | 18 (0.857) | 19 (0.905) | 18.5 (0.881) | 1.000 | 1.000 | 1.000 | 0 | 0 | 0 |
| quick | 14 (0.667) | 16 (0.762) | 14.5 (0.690) | 0.938† | 1.000 | 1.000 | 0 | 1† | 0 |

- Precision is matched ÷ (findings − known-issue findings), as the scorer computes it.
- The scorer's `false_positive_count` adds control false positives and unclassified findings together.
- The median of six runs is the mean of the 3rd and 4th values. The default median, 0.881, equals the `default-stability` report's recall.
- No run has two findings on one defect.

† **A01 in `quick-20261009-run-2` looks misclassified.** Finding F006 has element `calculator-paylater-checkbox`, `fr_text` "Payer maintenant", `en_text` "Pay later", fix "Payer plus tard", and the description `"Pay later" translated as "Pay now", opposite meaning; contradicts the help text about deferral.` That is A01's text and problem, but A01 is on `calculator-paylater-label`, so the scorer leaves the finding unclassified and marks A01 missed. Credited to A01, the run would be 16/21 (0.762), precision 1.000, 0 false positives, and the quick preset's recall median 15 (0.714). The figures above are the scorer's. Not changed in this task.

## 2. Per-defect detection (seeded build)

"d" is default and "q" is quick; "1008" and "1009" are the run dates (8 and 9 Oct), followed by the run number.

| id | category | d 1008 1 | d 1008 2 | d 1008 3 | d 1009 1 | d 1009 2 | d 1009 3 | default | q 1008 1 | q 1008 2 | q 1008 3 | q 1009 1 | q 1009 2 | q 1009 3 | quick |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D02 | placeholder | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D03 | hardcoded_text | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D04 | truncation | no | no | no | no | no | no | 0/6 | no | no | no | no | no | no | 0/6 |
| D05 | number_currency_format | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D06 | date_format | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D07 | lang_attribute | no | no | no | no | no | no | 0/6 | no | no | no | no | no | no | 0/6 |
| D08 | locale_navigation | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D09 | untranslated_validation | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| D10 | plural | yes | yes | yes | yes | yes | yes | 6/6 | yes | no‡ | yes | yes | yes | yes | 5/6 |
| G01 | terminology | no | yes | no | yes | yes | yes | 4/6 | no | no | no | no | no | no | 0/6 |
| G02 | terminology | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| G03 | terminology | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| G04 | register | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| A01 | mistranslation | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | no† | yes | 5/6 |
| A02 | mistranslation | yes | yes | yes | yes | yes | yes | 6/6 | yes | no | no | yes | yes | no | 3/6 |
| A03 | mistranslation | yes | yes | yes | yes | no | yes | 5/6 | no | no | no | no‡ | no‡ | no | 0/6 |
| A04 | mistranslation | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | no | yes | yes | yes | 5/6 |
| A05 | omission | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | yes | yes | yes | 6/6 |
| A06 | image_text | yes | yes | yes | yes | yes | yes | 6/6 | yes | yes | yes | no | yes | no | 4/6 |
| A07 | image_text | yes | yes | yes | yes | yes | yes | 6/6 | no | no | no | no | no | no | 0/6 |
| **total** | | **18** | **19** | **18** | **19** | **18** | **19** | | **16** | **14** | **14** | **15** | **15**† | **14** | |

† See § 1: a finding with A01's text and problem, filed on `calculator-paylater-checkbox`.

‡ **Named only in another finding's description.** These runs have no finding on the defect's element. The defect's text appears only in the description of the G02 finding on `dashboard-balance-label` (`fr_text` "Balance du compte"), which the scorer credits to G02. The scorer is right not to credit the second defect from it; the same case is labelled for A03 in G55 1 in `../20261001-sonnet55/comparison.md` § 2.
- `quick-20261008-run-2` F009, D10: `"Balance" is an anglicism for account balance; also "0 prêts actifs" should be "0 prêt actif".`
- `quick-20261009-run-1` F016 and `quick-20261009-run-2` F017, A03: `"Balance" is an anglicism for account balance; also "Déclaration mensuelle" should be "Relevé mensuel".`

The other misses have no finding that names the defect's element or its seeded text.

### Missed per preset

| preset | found in every run | missed in some runs | missed in every run |
|---|---|---|---|
| default | 17 | 2: G01 (missed 2/6: `default-20261008-run-1`, `-run-3`), A03 (missed 1/6: `default-20261009-run-2`) | 2: D04, D07 |
| quick | 11 | 5: A02 (missed 3/6), A06 (2/6), D10 (1/6‡), A01 (1/6†), A04 (1/6) | 5: D04, D07, G01, A03 (in 2 of the 6, named only in a G02 description ‡), A07 |

Quick misses by run: A02 in `quick-20261008-run-2`, `-run-3` and `quick-20261009-run-3`; A06 in `quick-20261009-run-1` and `-run-3`; D10 in `quick-20261008-run-2`; A01 in `quick-20261009-run-2`; A04 in `quick-20261008-run-3`.

Category not correct (detected, but the finding's category differs from the defect's): D01 in `default-20261009-run-1` and `quick-20261009-run-2`, `quick-20261008-run-3`; D03 in `default-20261008-run-2`, `default-20261009-run-2`, `-run-3` and `quick-20261008-run-1`; A03 in `default-20261008-run-3`; A04 in `quick-20261009-run-1`. Detection does not depend on category for these.

Matches without a testid (credited by text): D08 in `default-20261009-run-2` and `default-20261008-run-3` (link "Estimer un nouveau prêt", observed "/en/calculator"); A02 in `default-20261008-run-1` (`button "Proche"`). Every other defect match is by testid.

## 3. Clean build

| run | finding | page | element (testid after conversion) | category / severity | observed (`fr_text`) | scorer class | review note |
|---|---|---|---|---|---|---|---|
| `clean-default` | F001 | `/fr/nonexistent` | `heading "Not Found"` (none) | hardcoded_text / low | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 | The English 404 page under /fr/, as U03 describes. |
| `clean-default` | F002 | `/fr/dashboard` | `dashboard-due-date` | date_format / low | 2026-10-01 | unclassified (counted as a false positive) | False positive. The value is Babel's `fr_CA` short date (`date_short()` in `webapp/formatting.py`, `format="short"`), which is `2026-10-01`. C09's description calls it "a plain Babel short-date, not independently cataloged". The finding suggests "1 octobre 2026" to match the summary page's long date. |
| `clean-quick` | F001 | `/fr/calculator` | `calculator-early-repayment-note` | other / low | Aucuns frais ne s'appliquent au remboursement anticipé. | unclassified (counted as a false positive) | False positive. This is A04's `fr_clean`, the reference-correct text. The finding says "Aucuns frais" should be "Aucun frais". `frais` has no singular, so "aucuns frais" is a correct form. |
| `clean-quick` | F002 | `/fr/calculator` | `button "Calculateur de prêt"` (none) | mistranslation / medium | Calculateur de prêt | unclassified (counted as a false positive) | **Looks misclassified: this is U04.** The description reads `The recalculate button (testid calculator-recalculate-button) is labelled with the page title instead of an action; the English has the same flaw.` The adapter nulls a role-plus-name element, and U04 matches only by testid, so the finding is unclassified. Not changed in this task. |
| `clean-quick` | F003 | `/fr/dashboard` | `dashboard-due-date` | date_format / low | 2026-10-01 | unclassified (counted as a false positive) | False positive; the same finding as `clean-default` F002. |

| run | findings | known issue | control false positive | unclassified | `false_positive_count` |
|---|---|---|---|---|---|
| `clean-default` | 2 | 1 (U03) | 0 | 1 | 1 |
| `clean-quick` | 3 | 0 | 0 | 3 | 3 (2 if F002 is credited to U04) |

No clean finding landed on a control element, so neither run has a control false positive. The clean build has no defects, so no finding is credited to one.
