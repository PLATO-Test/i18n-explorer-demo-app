# i18n-explorer plugin 0.1.0 vs phase 3 POC explorer

Inputs:

- Plugin, seeded: `../i18n-explorer/i18n-explorer-runs/20260928-161518-localhost-5002/` (status `completed`)
- Plugin, clean: `../i18n-explorer/i18n-explorer-runs/20260928-161934-localhost-5001/` (status `completed`)
- POC explorer, seeded: `../i18n-qa/artifacts/20260923-v2/seeded/findings-ai-explorer-1.json`, `-2.json`, `-4.json` and `explorer/<n>/`
- POC explorer, clean: `../i18n-qa/artifacts/20260923-v2/clean/findings-ai-explorer-1.json` and `explorer/1/`

The plugin's `findings.json` files were converted with `scoring.adapters.plugin_v1` into
`seeded/findings.converted.json` and `clean/findings.converted.json`, then scored with `scoring.score`.
The source files were not modified; their SHA-256 checksums matched before and after conversion.
Both plugin runs use the same 16 category names as the scorer, so every category mapped 1:1 and none was unknown.
POC runs were scored one at a time with `scoring.matcher.score_run` against the same ground truth.

Both used an agent with `claude-sonnet-5` configured. The plugin has one seeded run. The POC has three.

## 1. Per-defect detection (seeded build)

| id | category | POC run 1 | POC run 2 | POC run 4 | POC total | plugin |
|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | 3/3 | yes |
| D02 | placeholder | yes | yes | yes | 3/3 | yes |
| D03 | hardcoded_text | yes | yes | yes | 3/3 | yes |
| D04 | truncation | no | no | no | 0/3 | no |
| D05 | number_currency_format | yes | yes | yes | 3/3 | yes |
| D06 | date_format | yes | yes | yes | 3/3 | yes |
| D07 | lang_attribute | no | no | no | 0/3 | no |
| D08 | locale_navigation | yes | yes | yes | 3/3 | yes |
| D09 | untranslated_validation | yes | yes | yes | 3/3 | yes |
| D10 | plural | yes | yes | yes | 3/3 | **no** |
| G01 | terminology | yes | no | no | 1/3 | no |
| G02 | terminology | yes | yes | yes | 3/3 | yes |
| G03 | terminology | yes | yes | yes | 3/3 | **no** |
| G04 | register | yes | yes | yes | 3/3 | yes |
| A01 | mistranslation | yes | yes | yes | 3/3 | yes |
| A02 | mistranslation | yes | yes | yes | 3/3 | yes |
| A03 | mistranslation | yes | yes | yes | 3/3 | yes |
| A04 | mistranslation | yes | yes | yes | 3/3 | yes |
| A05 | omission | yes | yes | yes | 3/3 | yes |
| A06 | image_text | yes | yes | yes | 3/3 | **no** |
| A07 | image_text | yes | yes | yes | 3/3 | yes |
| **total** | | **19/21** | **18/21** | **18/21** | | **15/21** |

Recall: plugin 0.714. POC 0.905, 0.857 and 0.857 (mean 0.873).

All 15 plugin detections are on defects the POC found in 3 of 3 runs.
The plugin missed D10, G03 and A06, which the POC found in 3 of 3 runs.
It also missed G01, which the POC found in 1 of 3, and D04 and D07, which the POC never found.

Seeded precision is 1.000 for the plugin. Its 15 findings all match a defect: no control false positives, no known-issue hits and no unclassified findings.
The POC runs had 0 control false positives and 0 unclassified findings across all three runs.
Each POC run also had one U03 hit (`/fr/nonexistent`).
The plugin did visit `/fr/nonexistent-page` in the seeded run (seq 73–74) but reported nothing there.

## 2. Plugin misses that the POC found in at least 2 of 3 runs

Method, from the plugin's seeded `trajectory.jsonl`:

- **Reached:** a row whose `path` is the defect's French page.
- **Examined:** a `read_page`, `inspect` or `page_info` call made on that page whose `result` contains the defect's seeded text.
  For A06, the seeded text is the image's `src` file name.
  For every row cited below, `result_chars` equals the length of the stored `result`, so the trajectory holds the full tool output.
- **Screenshots:** the images are not text, so they can't be searched. They are listed, but not counted as evidence that the defect was seen.

| id | page | reached (seq) | examining call that shows the defect | reported on the element? | classification |
|---|---|---|---|---|---|
| D10 | `/fr/dashboard` | 42, 43, 79, 80 | seq 43 `read_page`: `span "0 prêts actifs" [testid=dashboard-active-loans-count]`. Seq 80 is a full-page screenshot of the same page. | no | examined but not reported |
| G03 | `/fr/` | 0, 1, 2 | seq 1 `read_page`: `link "Appliquer pour un prêt" [testid=landing-cta-apply] -> /fr/apply` | no | examined but not reported |
| A06 | `/fr/` | 0, 1, 2 | seq 1 `read_page`: `img ... [testid=landing-banner-image] ... src=/static/img/banner-en.png`. No screenshot of `/fr/` was taken in this run, so the `src` attribute in that listing is the only evidence. | no | examined but not reported |

No miss was "not reached" or "reached but not examined".
In each case the defect's text was in a tool result that the agent received.
The trajectory shows no `report_finding` call on the element.

For context, the defects the POC missed in at least 2 of 3 runs, which fall outside the classification above:

- **G01:** `label "Adresse e-mail" [testid=apply-email-label]` appears in `read_page` at seq 7, 9 and 60, and the plugin did not report it.
- **D07:** the trajectory records `lang: en` for `/fr/application/AP-100482` at seq 17–18, which means the server logged the wrong language there.
  The agent made no `page_info` call on that page, and the `read_page` output does not include the document language.
  The finish summary says the lang and hreflang attributes were verified on multiple pages and were all correct.
  The plugin called `page_info` only on `/fr/` and `/fr/calculator`.
- **D04:** there is no text signal to search for. The plugin took 4 screenshots, none of them of `/fr/apply`.

## 3. Plugin findings that match no defect

Seeded build: none. All 15 findings match a defect.

Clean build: 3 findings.

| scorer class | page | testid | category | observed | expected | my classification |
|---|---|---|---|---|---|---|
| known issue (U03) | /fr/nonexistent-page | - | missing_translation | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | Serve a localized 404 page under /fr/ with French text and lang="fr-CA", matching the site's design. | known issue U03 |
| unclassified | /fr/dashboard | dashboard-active-loans-count | plural | 0 prêt actif | 0 prêt actifs | false positive |
| known issue (U05) | /fr/apply | apply-amount-input | number_currency_format | Entrez un montant entre 1 000,00 $ et 50 000,00 $. (shown when amount="15 000,50") | Accept French-Canadian number formatting (space as thousands separator, comma as decimal separator) in the loan amount field on the French site… | known issue U05 |

**Plural finding (false positive).** In French, zero takes the singular. Babel gives `Locale.parse('fr_CA').plural_form(0) == 'one'`, so "0 prêt actif" is correct.
The plugin's own `expected` value ("0 prêt actifs") contradicts its description ("0 prêts actifs").
In the seeded run, the same plugin read the actual plural error "0 prêts actifs" at seq 43 and did not report it (D10 above).

**Amount input (U05).** `webapp/routes/apply.py:67` parses the amount with a plain `float()` in every locale and in both builds, so the French form rejects "15 000,50".
This is a real, pre-existing behaviour, not seeded, and is now known issue U05 in `ground_truth/known_issues.yaml`.
U05 is page-level: any finding on `/fr/apply` in `number_currency_format`, `untranslated_validation` or `other` matches it.
Only the plugin reported this issue. No POC explorer run did, and neither did phase 1 or phase 2.

Clean-build false positives:

- **Scorer convention** (every clean finding that is not a known issue): plugin 1 (the plural finding), POC run 1 0 (its 2 findings were U03 and U04).
- **By manual review:** the same; the plural finding is a false positive.
- There is only one clean run of each, so neither FP rate is based on repeats.

## 4. Per-run activity

All figures below come from each run's own `trajectory.jsonl`, using the same method for every run.

| run | status | tool calls (budget) | report_finding | exploration calls | screenshots | duration (s) | findings | fr pages | en pages |
|---|---|---|---|---|---|---|---|---|---|
| POC seeded run 1 | completed | 79 | 20 | 58 | 4 | 106.4 | 20 | 5/5 | 5/5 |
| POC seeded run 2 | completed | 74 | 19 | 54 | 4 | 90.5 | 19 | 5/5 | 5/5 |
| POC seeded run 4 | completed | 76 | 19 | 56 | 2 | 126.0 | 19 | 5/5 | 5/5 |
| POC clean run 1 | completed | 76 | 2 | 73 | 2 | 85.8 | 2 | 5/5 | 5/5 |
| plugin seeded | completed | 86 | 15 | 70 | 4 | 209.4 | 15 | 5/5 | 5/5 |
| plugin clean | completed | 99 | 3 | 95 | 4 | 284.7 | 3 | 5/5 | 5/5 |

Notes:

- **Tool calls (budget):** the run's own budget counter.
  - It counts every tool call, including `report_finding` and `finish`.
  - The plugin's trajectory has one more row than the counter (87 and 100 rows): the `start_run` call is logged but not counted.
- **Exploration calls:** trajectory rows minus `report_finding`, `finish` and `start_run`. Only the plugin has an `inspect` tool; its clean run used it 4 times (2 returned errors).
- **Pages:**
  - A page counts as reached when a trajectory row's `path` is its page-map path. The page map has 5 pages: landing, apply, calculator, application summary and dashboard.
  - The English paths are the French paths with `/fr/` replaced by `/en/`.
  - The POC's own `coverage.json` reports 4/5 English pages because it does not credit the English summary page (see the phase 3 comparison). The trajectory shows that page was visited in every POC run.
- **Duration** is measured differently for each product:
  - Plugin: `start_run` to `finish`.
  - POC: the harness's session time from `manifest.json`.
- **Tokens and cost:** the plugin records none, so they are n/a.
