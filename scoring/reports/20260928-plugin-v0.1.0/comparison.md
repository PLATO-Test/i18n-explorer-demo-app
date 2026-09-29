# i18n-explorer plugin 0.1.0 vs phase 3 POC explorer

Inputs:

- Plugin, seeded, run 1: `../i18n-explorer/i18n-explorer-runs/20260928-161518-localhost-5002/` (status `completed`) → `seeded/`
- Plugin, seeded, run 2: `../i18n-explorer/i18n-explorer-runs/20260929-125402-localhost-5002/` (status `completed`) → `seeded-run-2/`
- Plugin, seeded, run 3: `../i18n-explorer/i18n-explorer-runs/20260929-125842-localhost-5002/` (status `completed`) → `seeded-run-3/`
- Plugin, seeded, runs 1–3 together → `seeded-stability/`
- Plugin, clean: `../i18n-explorer/i18n-explorer-runs/20260928-161934-localhost-5001/` (status `completed`) → `clean/`
- POC explorer, seeded: `../i18n-qa/artifacts/20260923-v2/seeded/findings-ai-explorer-1.json`, `-2.json`, `-4.json` and `explorer/<n>/`
- POC explorer, clean: `../i18n-qa/artifacts/20260923-v2/clean/findings-ai-explorer-1.json` and `explorer/1/`

The plugin's `findings.json` files were converted with `scoring.adapters.plugin_v1` into
`<folder>/findings.converted.json`, then scored with `scoring.score`.
The source files were not modified; their SHA-256 checksums matched before and after conversion.
Every plugin run uses the same 16 category names as the scorer, so every category mapped 1:1 and none was unknown.
The stability report scores copies of the three converted files together, the same way as the POC's
`20260923-v2/phase3-ai-explorer/seeded-stability/` (runs 1, 2 and 4 in one temporary folder).
POC runs were scored one at a time with `scoring.matcher.score_run` against the same ground truth.

**Element notation in plugin run 2.** Runs 1 and 3 write `element` as the bare testid (`site-footer`).
Run 2 writes it in the plugin's `read_page` notation (`[testid=site-footer]`, once `img [testid=landing-banner-image]`).
With the adapter as it was, run 2 scored 2/21 with 13 unclassified findings, because no testid matched.
The adapter now takes X from `[testid=X]` when it is the only testid in `element` (commit "Accept the [testid=X] element form in the plugin adapter").
Re-converting plugin run 1, run 3 and the clean run gives byte-identical output, and run 2 then scores 15/21 with no unclassified findings.
All run 2 figures below use the corrected conversion.

All runs used an agent with `claude-sonnet-5` configured. Each product has three seeded runs.

## 1. Per-defect detection (seeded build)

| id | category | POC 1 | POC 2 | POC 4 | POC | plugin 1 | plugin 2 | plugin 3 | plugin |
|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D02 | placeholder | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D04 | truncation | no | no | no | 0/3 | no | no | yes | 1/3 |
| D05 | number_currency_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D06 | date_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D07 | lang_attribute | no | no | no | 0/3 | no | no | no | 0/3 |
| D08 | locale_navigation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D10 | plural | yes | yes | yes | 3/3 | no | no | no | **0/3** |
| G01 | terminology | yes | no | no | 1/3 | no | no | no | 0/3 |
| G02 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G03 | terminology | yes | yes | yes | 3/3 | no | no | yes | **1/3** |
| G04 | register | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A01 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A02 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A03 | mistranslation | yes | yes | yes | 3/3 | yes | yes | no | 2/3 |
| A04 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A05 | omission | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A06 | image_text | yes | yes | yes | 3/3 | no | yes | yes | 2/3 |
| A07 | image_text | yes | yes | yes | 3/3 | yes | no | yes | 2/3 |
| **total** | | **19/21** | **18/21** | **18/21** | | **15/21** | **15/21** | **17/21** | |

### Recall per run

| | run 1 | run 2 | third run (POC 4, plugin 3) | range | mean |
|---|---|---|---|---|---|
| POC (runs 1, 2, 4) | 19 (0.905) | 18 (0.857) | 18 (0.857) | 18–19 | 18.3 (0.873) |
| plugin (runs 1, 2, 3) | 15 (0.714) | 15 (0.714) | 17 (0.810) | 15–17 | 15.7 (0.746) |

The two ranges do not overlap: the best plugin run (17) is one below the worst POC run (18).
Within each product, the spread is 1 defect for the POC and 2 for the plugin.

### Found in every run, some runs, none

| | every run | some runs | no run |
|---|---|---|---|
| POC | 18: D01, D02, D03, D05, D06, D08, D09, D10, G02, G03, G04, A01–A07 | 1: G01 (1/3) | 2: D04, D07 |
| plugin | 13: D01, D02, D03, D05, D06, D08, D09, G02, G04, A01, A02, A04, A05 | 5: A03, A06, A07 (2/3); D04, G03 (1/3) | 3: D07, D10, G01 |

- Every defect the plugin found in all three runs, the POC also found in all three.
- D04 is the only defect the plugin found that the POC never did (plugin run 3, `apply-submit-button`, evidence `screenshots/089.png`).
- D10 is the only defect the POC found in every run and the plugin found in none.

Seeded precision is 1.000 in all three plugin runs: every finding matches a defect, with no control false positives, no known-issue hits and no unclassified findings (after the run 2 conversion fix).
The POC runs had 0 control false positives and 0 unclassified findings across all three runs; each also had one U03 hit (`/fr/nonexistent`).
The plugin visited `/fr/nonexistent-page` in seeded run 1 (seq 73–74) and reported nothing there.

## 2. Plugin misses that the POC found in at least 2 of 3 runs

Qualifying defects (plugin missed in ≥2 of 3 runs, POC found in ≥2 of 3): **D10** (plugin 0/3, POC 3/3) and **G03** (plugin 1/3, POC 3/3).
D04 (plugin missed 2/3) and G01, D07 do not qualify, because the POC found them in fewer than 2 runs.
A03, A06 and A07 were each missed in only 1 plugin run.

Method, from each plugin run's seeded `trajectory.jsonl`:

- **Reached:** a row whose `path` is the defect's French page.
- **Examined:** a `read_page`, `inspect` or `page_info` call made on that page whose `result` contains the defect's seeded text.
  For every row cited below, `result_chars` equals the length of the stored `result`, so the trajectory holds the full tool output.
- **Reported:** a `report_finding` call whose element is the defect's testid.
- **Screenshots:** the images are not text, so they can't be searched. They are listed, but not counted as evidence that the defect was seen.

| id | page | run | reached (seq) | examining call that shows the defect | screenshots of the page | classification |
|---|---|---|---|---|---|---|
| D10 | `/fr/dashboard` | 1 | 42, 43, 79, 80 | seq 43 `read_page`: `span "0 prêts actifs" [testid=dashboard-active-loans-count]` | seq 80 | examined but not reported |
| D10 | `/fr/dashboard` | 2 | 48, 49, 58, 59 | seq 49 `read_page`: same line | none | examined but not reported |
| D10 | `/fr/dashboard` | 3 | 6, 7 | seq 7 `read_page`: same line | none | examined but not reported |
| G03 | `/fr/` | 1 | 0, 1, 2 | seq 1 `read_page`: `link "Appliquer pour un prêt" [testid=landing-cta-apply] -> /fr/apply` | none | examined but not reported |
| G03 | `/fr/` | 2 | 0, 1, 2, 5, 6 | seq 1 `read_page`: same line | seq 6 | examined but not reported |
| G03 | `/fr/` | 3 | 0, 1, 2, 55, 56, 58, 97, 98 | seq 1 `read_page`; seq 98 `inspect` | seq 56 | reported (seq 78, F016) |

- No miss was "not reached" or "reached but not examined".
  In each of the five misses, the defect's text was in a tool result the agent received, and there was no `report_finding` call on the element.
- In run 2, the agent quoted the G03 text in a different finding.
  Its register finding on `landing-hero-subtitle` (seq 9, matched to G04) lists "Appliquer pour un prêt" as an example of the site's formal "vous" register.
- In every run, the agent read `/en/dashboard` two calls after the French page ("0 active loans": run 1 seq 45, run 2 seq 51, run 3 seq 9).

For context, the defects the POC missed in at least 2 of 3 runs, which fall outside the classification above:

- **G01:** missed by the plugin in all three runs.
  In run 1, `label "Adresse e-mail" [testid=apply-email-label]` appears in `read_page` at seq 7, 9 and 60.
- **D07:** missed in all three runs.
  In run 1, the trajectory records `lang: en` for `/fr/application/AP-100482` at seq 17–18, and the agent made no `page_info` call on that page.
  Each run made 2 `page_info` calls.
- **D04:** found only in run 3, the one run that took a screenshot of `/fr/apply` (seq 89).
  The finding cites that screenshot. Runs 1 and 2 took no screenshot of `/fr/apply`.

## 3. Plural rule (French zero takes the singular)

CLDR/Babel: `Locale.parse('fr_CA').plural_form(0) == 'one'`, so the correct French text is "0 prêt actif".
The seeded build shows "0 prêts actifs" (D10); the clean build shows "0 prêt actif".

| run | build | text read on `/fr/dashboard` | reported | correct? |
|---|---|---|---|---|
| plugin 1 | seeded | "0 prêts actifs" (seq 43) | no | no: the plural error was missed |
| plugin 2 | seeded | "0 prêts actifs" (seq 49) | no | no: the plural error was missed |
| plugin 3 | seeded | "0 prêts actifs" (seq 7) | no | no: the plural error was missed |
| plugin clean | clean | "0 prêt actif" (seq 39) | yes (seq 42, plural finding) | no: the correct singular was reported as an error |

In the three seeded runs, no `report_finding` call and no finish summary contains "plural", "pluriel", "singular", "prêt actif" or "active loans".
The trajectory records tool calls only, not the agent's reasoning, so it does not show whether the agent considered the line.
In the one clean run, the agent reported the correct singular as wrong, with an `expected` value ("0 prêt actifs") that contradicts its own description ("0 prêts actifs").
The POC reported "0 prêts actifs" on the seeded build in 3 of 3 runs and made no plural finding on its clean run.

## 4. Plugin findings that match no defect

Seeded build: none in any of the three runs.

Clean build: 3 findings.

| scorer class | page | testid | category | observed | expected | my classification |
|---|---|---|---|---|---|---|
| known issue (U03) | /fr/nonexistent-page | - | missing_translation | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | Serve a localized 404 page under /fr/ with French text and lang="fr-CA", matching the site's design. | known issue U03 |
| unclassified | /fr/dashboard | dashboard-active-loans-count | plural | 0 prêt actif | 0 prêt actifs | false positive |
| known issue (U05) | /fr/apply | apply-amount-input | number_currency_format | Entrez un montant entre 1 000,00 $ et 50 000,00 $. (shown when amount="15 000,50") | Accept French-Canadian number formatting (space as thousands separator, comma as decimal separator) in the loan amount field on the French site… | known issue U05 |

**Plural finding (false positive).** See section 3.

**Amount input (U05).** `webapp/routes/apply.py:67` parses the amount with a plain `float()` in every locale and in both builds, so the French form rejects "15 000,50".
This is a real, pre-existing behaviour, not seeded, and is now known issue U05 in `ground_truth/known_issues.yaml`.
U05 matches findings on `/fr/apply` whose testid is `apply-amount-input` or `apply-error-amount`, in `number_currency_format`, `untranslated_validation` or `other`.
Only the plugin reported this issue. No POC explorer run did, and neither did phase 1 or phase 2.

Clean-build false positives:

- **Scorer convention** (every clean finding that is not a known issue): plugin 1 (the plural finding), POC run 1 0 (its 2 findings were U03 and U04).
- **By manual review:** the same; the plural finding is a false positive.
- There is only one clean run of each, so neither FP rate is based on repeats.

## 5. Per-run activity

All figures below come from each run's own `trajectory.jsonl`, using the same method for every run.

| run | status | tool calls (budget) | report_finding | exploration calls | screenshots | duration (s) | findings | fr pages | en pages |
|---|---|---|---|---|---|---|---|---|---|
| POC seeded run 1 | completed | 79 | 20 | 58 | 4 | 106.4 | 20 | 5/5 | 5/5 |
| POC seeded run 2 | completed | 74 | 19 | 54 | 4 | 90.5 | 19 | 5/5 | 5/5 |
| POC seeded run 4 | completed | 76 | 19 | 56 | 2 | 126.0 | 19 | 5/5 | 5/5 |
| POC clean run 1 | completed | 76 | 2 | 73 | 2 | 85.8 | 2 | 5/5 | 5/5 |
| plugin seeded run 1 | completed | 86 | 15 | 70 | 4 | 209.4 | 15 | 5/5 | 5/5 |
| plugin seeded run 2 | completed | 84 | 15 | 68 | 3 | 244.0 | 15 | 5/5 | 5/5 |
| plugin seeded run 3 | completed | 99 | 17 | 81 | 5 | 274.7 | 17 | 5/5 | 5/5 |
| plugin clean | completed | 99 | 3 | 95 | 4 | 284.7 | 3 | 5/5 | 5/5 |

Notes:

- **Tool calls (budget):** the run's own budget counter.
  - It counts every tool call, including `report_finding` and `finish`.
  - The plugin's trajectory has one more row than the counter: the `start_run` call is logged but not counted.
- **Exploration calls:** trajectory rows minus `report_finding`, `finish` and `start_run`.
  Only the plugin has an `inspect` tool: seeded run 1 used it 0 times, run 2 3 times (2 returned errors), run 3 5 times, the clean run 4 times (2 errors).
- **Pages:**
  - A page counts as reached when a trajectory row's `path` is its page-map path. The page map has 5 pages: landing, apply, calculator, application summary and dashboard.
  - The English paths are the French paths with `/fr/` replaced by `/en/`.
  - The POC's own `coverage.json` reports 4/5 English pages because it does not credit the English summary page (see the phase 3 comparison). The trajectory shows that page was visited in every POC run.
- **Duration** is measured differently for each product:
  - Plugin: `start_run` to `finish`.
  - POC: the harness's session time from `manifest.json`.
- **Tokens and cost:** the plugin records none, so they are n/a.
