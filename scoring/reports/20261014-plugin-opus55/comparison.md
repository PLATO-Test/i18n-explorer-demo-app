# i18n-explorer default preset: Claude Opus 5.5 vs Claude Sonnet 5.5

This compares two groups. Each has three seeded runs and one clean run, all with the default preset (effort high), headless, at viewport 1920×1080.

- **Opus 5.5:** plugin 0.5.3 with the default agent and preset switched to `claude-opus-5-5`, run on 14 October. Run setup is in `project/05.11-opus55-experiment.md`.
- **Sonnet 5.5:** the plugin 0.5.1 measurement on `claude-sonnet-5-5`, run on 9 October (05.10 group A and C default). Its scores are in `../20261009-plugin-v0.5/` (`default-20261009-run-1..3`, `clean-default`).

The 0.5.0 runs from 8 October are not part of this comparison.

The two groups differ in more than the model:

- **Plugin version: 0.5.3 vs 0.5.1.** `git diff v0.5.1 v0.5.3` in the plugin repo changes no file under `agents/`, `skills/` or `commands/`, apart from the model line that 05.11 changed in its copy. The server changes are:
  - the origin lock is set after redirects;
  - off-site redirects are refused;
  - the `start_run` message has one more field, `site {origin}`;
  - `run.typed_origin` and `run.effective_origin` were added (findings schema 1.3.0).
- **Claude Code:** 2.1.300 vs 2.1.295.
- **Date:** 14 October vs 9 October.

This document does not attribute any difference to any of these factors.

## Inputs

| group | build | run | source | plugin | status | model observed | effort observed | report |
|---|---|---|---|---|---|---|---|---|
| Opus | seeded | 1 | `i18n-explorer/i18n-explorer-runs/20261014-161128-localhost-5002/findings.json` | 0.5.3 | completed | claude-opus-5-5 (43) | high (43) | `run-1/` |
| Opus | seeded | 2 | `i18n-explorer/i18n-explorer-runs/20261014-161643-localhost-5002/findings.json` | 0.5.3 | completed | claude-opus-5-5 (38) | high (38) | `run-2/` |
| Opus | seeded | 3 | `i18n-explorer/i18n-explorer-runs/20261014-162158-localhost-5002/findings.json` | 0.5.3 | completed | claude-opus-5-5 (33) | high (33) | `run-3/` |
| Opus | seeded | all three | the three converted files | | | | | `stability/` |
| Opus | clean | 1 | `i18n-explorer/i18n-explorer-runs/20261014-162641-localhost-5001/findings.json` | 0.5.3 | completed | claude-opus-5-5 (33) | high (33) | `clean/` |
| Sonnet | seeded | 1 | `…\i18n-measure\v051-A-default-1\i18n-explorer-runs\20261009-092740-localhost-5002\findings.json` | 0.5.1 | completed | claude-sonnet-5-5 (23) | high (23) | `../20261009-plugin-v0.5/default-20261009-run-1/` |
| Sonnet | seeded | 2 | `…\i18n-measure\v051-A-default-2\i18n-explorer-runs\20261009-093012-localhost-5002\findings.json` | 0.5.1 | completed | claude-sonnet-5-5 (19) | high (19) | `../20261009-plugin-v0.5/default-20261009-run-2/` |
| Sonnet | seeded | 3 | `…\i18n-measure\v051-A-default-3\i18n-explorer-runs\20261009-093216-localhost-5002\findings.json` | 0.5.1 | completed | claude-sonnet-5-5 (21) | high (21) | `../20261009-plugin-v0.5/default-20261009-run-3/` |
| Sonnet | clean | 1 | `…\i18n-measure\v051-C-default\i18n-explorer-runs\20261009-093920-localhost-5001\findings.json` | 0.5.1 | completed | claude-sonnet-5-5 (19) | high (19) | `../20261009-plugin-v0.5/clean-default/` |

The Opus paths are relative to the repo root (`C:\Users\AlexHotvianskyi\dev\ai-multilingual-poc\`). In the Sonnet paths, `…` stands for `C:\Users\AlexHotvianskyi\AppData\Local\Temp`. "Model observed" and "effort observed" are from `run.observed`. The subagent transcripts agree: every Opus response is `claude-opus-5-5` with `perTurnEffort` `high`, and every Sonnet response is `claude-sonnet-5-5` with `perTurnEffort` `high`.

How the Opus runs were scored:

- Each Opus file was converted with `scoring.adapters.plugin_v1` and scored with `scoring.score`. The converted output is kept as `<report>/findings.converted.json`.
- The adapter needed no change for findings schema 1.3.0. That version adds only the optional `run.typed_origin` and `run.effective_origin`, which the adapter does not read, and all four converted files passed the scorer's schema check.
- `stability/` scores the three seeded `findings.converted.json` files together. They were copied into one folder outside the repo for that run.

Checks on the inputs and on the baseline:

- The SHA-256 of every source findings.json matched 05.10 or 05.11 before scoring and was unchanged after it.
- The Sonnet group was not converted again. It was re-scored from its committed `findings.converted.json` files into a scratch folder with the current scorer, and all four `report.json` files equal the committed ones as JSON.

## 1. Recall and precision per run (seeded build)

| group | run | findings | matched a defect | known issue | control false positive | unclassified | recall | precision |
|---|---|---|---|---|---|---|---|---|
| Opus | `run-1` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus | `run-2` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus | `run-3` | 22 | 21 | 1 (U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Sonnet | `default-20261009-run-1` | 20 | 19 | 1 (U03) | 0 | 0 | 19/21 (0.905) | 1.000 |
| Sonnet | `default-20261009-run-2` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 |
| Sonnet | `default-20261009-run-3` | 21 | 19 | 2 (U03, U04) | 0 | 0 | 19/21 (0.905) | 1.000 |

| group | recall min | recall max | recall mean | precision (every run) |
|---|---|---|---|---|
| Opus | 21 (1.000) | 21 (1.000) | 21.0 (1.000) | 1.000 |
| Sonnet | 18 (0.857) | 19 (0.905) | 18.67 (0.889) | 1.000 |

- Precision is matched ÷ (findings − known-issue findings), as the scorer computes it. No run in either group has a control false positive or an unclassified finding.
- No run has two findings on one defect.
- U05 (the French apply form rejects amounts typed in fr-CA format) appears in all three Opus seeded runs and in none of the three Sonnet runs. It is a known issue, so it counts toward neither recall nor precision.

## 2. Per-defect detection (seeded build)

| id | category | Sonnet 1 | Sonnet 2 | Sonnet 3 | Sonnet | Opus 1 | Opus 2 | Opus 3 | Opus |
|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D02 | placeholder | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **D04** | truncation | no | no | no | **0/3** | yes | yes | yes | **3/3** |
| D05 | number_currency_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D06 | date_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **D07** | lang_attribute | no | no | no | **0/3** | yes | yes | yes | **3/3** |
| D08 | locale_navigation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D10 | plural | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G01 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G02 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G03 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G04 | register | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A01 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A02 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **A03** | mistranslation | yes | no | yes | **2/3** | yes | yes | yes | **3/3** |
| A04 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A05 | omission | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A06 | image_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A07 | image_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **total** | | **19** | **18** | **19** | | **21** | **21** | **21** | |

The three rows in bold are the ones where the groups differ. The other 18 defects were found in all six runs.

- **A03 in Sonnet run 2:** no finding names `dashboard-statement-link` or "Déclaration mensuelle" (`../20261009-plugin-v0.5/comparison.md` § 2).
- **Category not correct:** the defect was detected, but the finding's category differs from the defect's. Detection does not depend on category for these. Cases:
  - Sonnet: D01 in run 1, and D03 in runs 2 and 3.
  - Opus: D03 in runs 1 and 3.
- **Match by testid:** every defect match in both groups is by testid except these, which the scorer credits by its other rules:
  - D07 in all three Opus runs, by category on the summary page.
  - D08 in Sonnet run 2, by text. Its element, `link "Estimer un nouveau prêt" [testid=dashboard-estimate-loan-link]`, combines a role, a name and a testid, and the adapter turns that form into null.

## 3. D04 and D07

### Found or not

| defect | Sonnet 1 | Sonnet 2 | Sonnet 3 | Opus 1 | Opus 2 | Opus 3 |
|---|---|---|---|---|---|---|
| D04 (`/fr/apply`, `apply-submit-button`) | missed | missed | missed | found (F005) | found (F006) | found (F006) |
| D07 (`/fr/application/AP-100482`, `html lang`) | missed | missed | missed | found (F009) | found (F021) | found (F021) |

### Trajectory, per run

Seq numbers are from each run's `trajectory.jsonl`.

The Sonnet runs below are reads of the 9 October trajectories, using the same method as `../20261001-sonnet55/comparison.md` and `project/05.3-plugin-vs-poc-scoring.md`.

| defect | run | rows on the page | `read_page` that shows the button / page | screenshot of `/fr/apply` | `inspect` on `apply-submit-button` | `page_info` on the summary page | finding | classification |
|---|---|---|---|---|---|---|---|---|
| D04 | Sonnet 1 | 11, from seq 10 | 11, 13, 20 | none | none | – | none | missed: examined by `read_page` (the label text is correct in both builds); no screenshot of `/fr/apply`; no `inspect` |
| D04 | Sonnet 2 | 17, from seq 14 | 16, 25 | none | none | – | none | missed: same as run 1 |
| D04 | Sonnet 3 | 18, from seq 10 | 11, 13, 20 | none | none | – | none | missed: same as run 1 |
| D04 | Opus 1 | 30, from seq 11 | 12, 20, 28, 103 | seq 16 | seq 17 | – | F005, evidence `screenshots/016.png`, seq 17 | found |
| D04 | Opus 2 | 28, from seq 11 | 12, 19, 30, 103 | seq 22 | seq 21 | – | F006, evidence `screenshots/022.png`, seq 22 | found |
| D04 | Opus 3 | 29, from seq 11 | 12, 19, 32, 101 | seq 23 | seq 21 | – | F006, evidence `screenshots/023.png`, seq 23 | found |
| D07 | Sonnet 1 | 2, entered by `navigate` at seq 40 | 41 | – | – | none | none | missed: reached; no `page_info` call on the page |
| D07 | Sonnet 2 | 2, entered by click at seq 40 | 41 | – | – | none | none | missed: same as run 1 |
| D07 | Sonnet 3 | 2, entered by click at seq 33 | 34 | – | – | none | none | missed: same as run 1 |
| D07 | Opus 1 | 4, entered by click at seq 44 | 45 | – | – | seq 46 (`html lang: en`) | F009, evidence seq 46 | found |
| D07 | Opus 2 | 4, entered by click at seq 47 | 48 | – | – | seq 87 (`html lang: en`), after a `navigate` back at seq 86 | F021, evidence seq 87 | found |
| D07 | Opus 3 | 4, entered by click at seq 48 | 49 | – | – | seq 89 (`html lang: en`), after a `navigate` back at seq 88 | F021, evidence seq 89 | found |

- **Sonnet `page_info` and `inspect` calls:**
  - Every `page_info` call, by run: run 1 at seq 2 (`/fr/`) and seq 82 (`/en/dashboard`); runs 2 and 3 only at seq 2 (`/fr/`).
  - None of the three runs made an `inspect` call.
  - No Sonnet finding contains "Soumettre", "lang=", "html lang", "truncat" or "clipp".
- **Sonnet screenshots:**
  - Run 1: `/en/` and `/fr/calculator`.
  - Run 2: `/en/`, `/en/calculator` and `/fr/calculator`.
  - Run 3: `/en/`, `/fr/calculator` and `/en/calculator`.
- **Opus `page_info` calls:** each Opus run called `page_info` on 6 to 8 pages, in both locales. Each also checked the English summary page, except run 3. Every `page_info` call, by run:
  - Run 1: `/fr/`, `/fr/application/AP-100482`, `/fr/calculator`, `/fr/dashboard`, `/en/application/AP-100482`, `/en/dashboard`.
  - Run 2: `/fr/`, `/fr/calculator`, `/fr/application/AP-100482`, `/fr/dashboard`, `/fr/apply`, `/en/application/AP-100482`, `/en/dashboard`, `/en/calculator`.
  - Run 3: `/fr/`, `/fr/calculator`, `/fr/dashboard`, `/fr/application/AP-100482`, `/fr/apply`, `/en/calculator`, `/en/dashboard`.
- **Opus D04 findings:**
  - All three cite the `inspect` measurement: "scrollWidth 290 > clientWidth 210, overflow hidden, nowrap".
  - Each D04 finding cites both a screenshot of `/fr/apply` and that `inspect` result.
  - In run 1 the screenshot came before the `inspect`; in runs 2 and 3 it came after.

## 4. Clean build

| group | finding | page | element (testid after conversion) | category / severity | observed | scorer class |
|---|---|---|---|---|---|---|
| Opus | F001 | `/fr/apply` | `apply-amount-input` | number_currency_format / medium | 12500,50 → "Entrez un montant entre 1 000,00 $ et 50 000,00 $." | known issue U05 |
| Opus | F002 | `/fr/dashboard` | `dashboard-recent-transactions-count` | terminology / low | 3 opérations récentes / Transactions récentes | known issue U02 |
| Opus | F003 | `/fr/introuvable` | none | hardcoded_text / medium | 404 Not Found / Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Sonnet | F001 | `/fr/nonexistent` | none | hardcoded_text / low | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Sonnet | F002 | `/fr/dashboard` | `dashboard-due-date` | date_format / low | 2026-10-01 | unclassified (counted as a false positive) |

| group | findings | known issue | false positive (control) | unclassified | `false_positive_count` |
|---|---|---|---|---|---|
| Opus | 3 | 3 (U02, U03, U05) | 0 | 0 | 0 |
| Sonnet | 2 | 1 (U03) | 0 | 1 | 1 |

- **Opus F002 (U02):** the finding's description reads: `The same English term "transactions" is translated as "opérations" in the counter and as "Transactions" in the section heading on the same page; "opérations" is the preferred Quebec banking term.` That is U02 as `known_issues.yaml` describes it.
- **Sonnet F002:** a false positive. The value is Babel's `fr_CA` short date. It was reviewed in `../20261009-plugin-v0.5/comparison.md` § 3.

## 5. Behaviour and cost per run

Sources:

- **Model turns:** the distinct `message.id`s in the subagent transcript.
- **Tool calls:** the `tool_use` blocks in those turns. The server's budget counter, in parentheses, is one lower in every run of both groups.
- **Screenshots:** the `screenshot` calls in `trajectory.jsonl`.
- **Tokens and cost:** the stream log's `result` event, `modelUsage`. Thinking is `thinkingTokens` as `modelUsage` reports it. Cost is `costUSD`, which equals `total_cost_usd` in every run: the CLI's notional figure at list price (`costBasis: list`).
- **Duration:** `run.duration_s`, the server's time from `start_run` to `finish`.

Cache writes are all 5-minute writes (05.10, 05.11).

| group | run | model turns | tool calls (budget) | screenshots | input | output | thinking | cache read | cache write | duration (s) | cost (USD) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sonnet | seeded 1 | 24 | 84 (83) | 2 | 48 | 14,161 | 1,101 | 590,214 | 46,452 | 121.2 | 0.376 |
| Sonnet | seeded 2 | 20 | 79 (78) | 3 | 40 | 13,014 | 788 | 436,068 | 41,258 | 108.0 | 0.321 |
| Sonnet | seeded 3 | 22 | 74 (73) | 3 | 44 | 12,905 | 860 | 514,652 | 40,930 | 113.3 | 0.334 |
| Sonnet | clean | 20 | 70 (69) | 4 | 40 | 7,014 | 890 | 446,877 | 39,231 | 83.3 | 0.258 |
| Opus | seeded 1 | 44 | 109 (108) | 4 | 88 | 17,177 | 1,567 | 1,435,609 | 59,376 | 271.6 | 0.928 |
| Opus | seeded 2 | 39 | 110 (109) | 4 | 78 | 17,230 | 1,795 | 1,280,422 | 55,611 | 280.6 | 0.879 |
| Opus | seeded 3 | 34 | 107 (106) | 4 | 68 | 17,550 | 1,585 | 1,024,463 | 54,006 | 243.2 | 0.826 |
| Opus | clean | 34 | 98 (97) | 5 | 68 | 10,078 | 1,507 | 1,014,398 | 52,252 | 224.1 | 0.666 |

Seeded runs, mean (min–max):

| | Sonnet | Opus | Opus ÷ Sonnet (means) |
|---|---|---|---|
| model turns | 22 (20–24) | 39 (34–44) | 1.77 |
| tool calls | 79 (74–84) | 108.7 (107–110) | 1.38 |
| screenshots | 2.7 (2–3) | 4 (4–4) | 1.50 |
| output tokens | 13,360 (12,905–14,161) | 17,319 (17,177–17,550) | 1.30 |
| thinking tokens | 916 (788–1,101) | 1,649 (1,567–1,795) | 1.80 |
| cache read tokens | 513,645 (436,068–590,214) | 1,246,831 (1,024,463–1,435,609) | 2.43 |
| duration (s) | 114.2 (108.0–121.2) | 265.1 (243.2–280.6) | 2.32 |
| cost (USD) | 0.344 (0.321–0.376) | 0.878 (0.826–0.928) | 2.55 |
| cost per defect found (USD) | 0.0184 | 0.0418 | 2.27 |

- **Sonnet cache-read price:**
  - The CLI priced Sonnet cache reads at $0.20 per MTok, the figure 05.10 used. 05.11 notes that the current pricing page lists $0.10.
  - At $0.10, the Sonnet seeded costs would be $0.317, $0.277 and $0.283 (mean $0.292), and the clean run $0.213.
  - Opus ÷ Sonnet mean cost would then be 3.00 instead of 2.55.
  - The Opus figures do not change: they are already at $0.20, which is 5% of $4.
- **Tool-call budget:** both groups stayed under the 120 limit. Opus used 106–109 calls (budget counter), Sonnet 73–83. No run exhausted the budget (`exhausted` is null).
