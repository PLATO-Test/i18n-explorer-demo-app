# i18n-explorer 0.6.0: the four presets, measured on one day

This scores the plugin 0.6.0 preset measurement of 16 October (`project/05.13-v0.6.0-preset-measurement.md`): four presets, each with three seeded runs and one clean run, all headless at viewport 1920×1080, plugin tag `v0.6.0` (`c5c435d`), Claude Code 2.1.301.

| preset | skill | agent | model | effort |
|---|---|---|---|---|
| default | `/i18n-explore` | `explorer` | claude-sonnet-5-5 | high |
| quick | `/i18n-explore-quick` | `explorer-quick` | claude-sonnet-5-5 | medium |
| opus-low | `/i18n-explore-opus-low` | `explorer-opus-low` | claude-opus-5-5 | low |
| opus-medium | `/i18n-explore-opus-medium` | `explorer-opus-medium` | claude-opus-5-5 | medium |

§ 6 compares each preset with its earlier measurement. This document does not attribute any difference to any factor.

## Inputs

| preset | build | run | run_id (05.13 label) | status | model observed | effort observed | findings | report |
|---|---|---|---|---|---|---|---|---|
| default | seeded | 1 | `20261016-135558-localhost-5002` (1D) | completed | claude-sonnet-5-5 (19) | high (19) | 19 | `default/run-1/` |
| default | seeded | 2 | `20261016-140822-localhost-5002` (2D) | completed | claude-sonnet-5-5 (21) | high (21) | 21 | `default/run-2/` |
| default | seeded | 3 | `20261016-152403-localhost-5002` (3Db) | completed | claude-sonnet-5-5 (19) | high (19) | 19 | `default/run-3/` |
| default | clean | 1 | `20261016-153317-localhost-5001` (4D) | completed | claude-sonnet-5-5 (27) | high (27) | 2 | `default/clean/` |
| quick | seeded | 1 | `20261016-135857-localhost-5002` (1Q) | completed | claude-sonnet-5-5 (14) | medium (14) | 17 | `quick/run-1/` |
| quick | seeded | 2 | `20261016-141105-localhost-5002` (2Q) | completed | claude-sonnet-5-5 (15) | medium (15) | 17 | `quick/run-2/` |
| quick | seeded | 3 | `20261016-152613-localhost-5002` (3Q) | completed | claude-sonnet-5-5 (13) | medium (13) | 15 | `quick/run-3/` |
| quick | clean | 1 | `20261016-153505-localhost-5001` (4Q) | completed | claude-sonnet-5-5 (13) | medium (13) | 1 | `quick/clean/` |
| opus-low | seeded | 1 | `20261016-140120-localhost-5002` (1L) | completed | claude-opus-5-5 (19) | low (19) | 21 | `opus-low/run-1/` |
| opus-low | seeded | 2 | `20261016-141318-localhost-5002` (2L) | completed | claude-opus-5-5 (24) | low (24) | 21 | `opus-low/run-2/` |
| opus-low | seeded | 3 | `20261016-152731-localhost-5002` (3L) | completed | claude-opus-5-5 (20) | low (20) | 20 | `opus-low/run-3/` |
| opus-low | clean | 1 | `20261016-153604-localhost-5001` (4L) | completed | claude-opus-5-5 (26) | low (26) | 2 | `opus-low/clean/` |
| opus-medium | seeded | 1 | `20261016-140405-localhost-5002` (1M) | completed | claude-opus-5-5 (32) | medium (32) | 22 | `opus-medium/run-1/` |
| opus-medium | seeded | 2 | `20261016-141629-localhost-5002` (2M) | completed | claude-opus-5-5 (31) | medium (31) | 23 | `opus-medium/run-2/` |
| opus-medium | seeded | 3 | `20261016-152945-localhost-5002` (3M) | completed | claude-opus-5-5 (26) | medium (26) | 23 | `opus-medium/run-3/` |
| opus-medium | clean | 1 | `20261016-153832-localhost-5001` (4M) | completed | claude-opus-5-5 (35) | medium (35) | 3 | `opus-medium/clean/` |

Sources are `i18n-explorer/i18n-explorer-runs/<run_id>/findings.json`, relative to the repo root (`C:\Users\AlexHotvianskyi\dev\ai-multilingual-poc\`). "Model observed" and "effort observed" are from `run.observed`. In every file, `run.preset`, `model_configured` and `effort_configured` match the preset, and `run.observed.effort_at_stop` equals the configured effort. The failed first attempt of default run 3 (3D) has no run folder and is not scored.

How the runs were scored:

- Each file was converted with `scoring.adapters.plugin_v1` and scored with `scoring.score`. The converted output is kept as `<report>/findings.converted.json`. Neither the adapter nor the scorer was changed.
- `<preset>/stability/` scores the preset's three seeded `findings.converted.json` files together. They were copied into one folder outside the repo for that run.
- The SHA-256 of all 16 source files matched 05.13 before scoring and was unchanged after it.
- All figures below are the scorer's, except where marked "by hand".

## 1. Recall and precision per run (seeded build)

| preset | run | findings | matched a defect | known issue | control false positive | unclassified | recall | precision |
|---|---|---|---|---|---|---|---|---|
| default | `run-1` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 |
| default | `run-2` | 21 | 19 | 1 (U03) | 0 | 1 | 19/21 (0.905) | 0.950 |
| default | `run-3` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 |
| quick | `run-1` | 17 | 17 | 0 | 0 | 0 | 17/21 (0.810) | 1.000 |
| quick | `run-2` | 17 | 16 | 1 (U04) | 0 | 0 | 16/21 (0.762) | 1.000 |
| quick | `run-3` | 15 | 15 | 0 | 0 | 0 | 15/21 (0.714) | 1.000 |
| opus-low | `run-1` | 21 | 20 | 1 (U04) | 0 | 0 | 20/21 (0.952) | 1.000 |
| opus-low | `run-2` | 21 | 20 | 1 (U04) | 0 | 0 | 20/21 (0.952) | 1.000 |
| opus-low | `run-3` | 20 | 20 | 0 | 0 | 0 | 20/21 (0.952) | 1.000 |
| opus-medium | `run-1` | 22 | 21 | 1 (U03) | 0 | 0 | 21/21 (1.000) | 1.000 |
| opus-medium | `run-2` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| opus-medium | `run-3` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |

| preset | recall per run | range | mean | precision per run | `stability/` precision / recall |
|---|---|---|---|---|---|
| default | 18 / 19 / 18 | 18–19 | 18.33 (0.873) | 1.000 / 0.950 / 1.000 | 0.983 / 0.873 |
| quick | 17 / 16 / 15 | 15–17 | 16.00 (0.762) | 1.000 / 1.000 / 1.000 | 1.000 / 0.762 |
| opus-low | 20 / 20 / 20 | 20–20 | 20.00 (0.952) | 1.000 / 1.000 / 1.000 | 1.000 / 0.952 |
| opus-medium | 21 / 21 / 21 | 21–21 | 21.00 (1.000) | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 |

- Precision is matched ÷ (findings − known-issue findings), as the scorer computes it. No run has a control false positive. No run has two findings credited to one defect.
- **Default run 2, the one unclassified finding:** F020, `date_format`, `/fr/dashboard`, `dashboard-due-date`, `fr_text` "2026-10-01", fix "1er octobre 2026", description `Due date identical to the English; inconsistent with the French long date format used on the application page and with the other dashboard dates.` It is the same finding as the 05.10 clean-build false positive (`../20261009-plugin-v0.5/comparison.md` § 3): the value is Babel's `fr_CA` short date, the same in both builds, and no defect or control covers it. The scorer counts it as a false positive, which gives the run its precision of 0.950.
- **Known issues in the seeded runs:**
  - U03 (the default English 404 page under `/fr/`): all three default runs (`/fr/nonexistent`; `fr_text` "Not Found / The requested URL was not found on the server. …" in run 1, "Not Found" in run 2, "Not Found / The requested URL was not found on the server." in run 3) and all three opus-medium runs (`/fr/inexistant`, "Not Found — The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.").
  - U04 (the recalculate button labelled with the page title): quick run 2, opus-low runs 1 and 2 (`calculator-recalculate-button`, "Calculateur de prêt").
  - U05 (the French apply form rejects fr-CA amounts): opus-medium run 2 (`12500,50 → "Entrez un montant entre 1 000,00 $ et 50 000,00 $."`) and run 3 (`12 500,50 -> « Entrez un montant entre 1 000,00 $ et 50 000,00 $. »`).
  - Known issues count toward neither recall nor precision.

## 2. Per-defect detection (seeded build)

The six rows where the presets differ. The other 15 defects (D01, D02, D03, D05, D06, D08, D09, G02, G03, G04, A01, A02, A04, A05, A06) were found in all twelve runs.

| id | category | default 1 | default 2 | default 3 | default | quick 1 | quick 2 | quick 3 | quick | opus-low 1 | opus-low 2 | opus-low 3 | opus-low | opus-medium 1 | opus-medium 2 | opus-medium 3 | opus-medium |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D04 | truncation | no | no | no | 0/3 | no | no | no | 0/3 | no | yes | yes | 2/3 | yes | yes | yes | 3/3 |
| D07 | lang_attribute | no | no | no | 0/3 | no | no | no | 0/3 | yes | no | no | 1/3 | yes | yes | yes | 3/3 |
| D10 | plural | yes | yes | yes | 3/3 | yes | yes | no | 2/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G01 | terminology | no | yes | yes | 2/3 | no | no | no | 0/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A03 | mistranslation | yes | yes | no‡ | 2/3 | yes | no | no | 1/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A07 | image_text | yes | yes | yes | 3/3 | no | no | no | 0/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **total** | | **18** | **19** | **18** | | **17** | **16** | **15** | | **20** | **20** | **20** | | **21** | **21** | **21** | |

‡ **Named only in another finding's description.** Default run 3 has no finding on `dashboard-statement-link`. "Déclaration mensuelle" appears only in the description of F018, the G02 finding on `dashboard-balance-label` (`fr_text` "Balance du compte"), which the scorer credits to G02. This is the same case as the ‡ rows in `../20261009-plugin-v0.5/comparison.md` § 2.

- **The other misses** have no finding that names the defect's element or text. The findings of each run were searched for the element and for its French text.
- **opus-low trajectory facts, from `trajectory.jsonl`:**
  - Run 1 (D04 missed) made no `inspect` call and took no screenshot of `/fr/apply`. Its one screenshot was of `/fr/calculator`. It called `page_info` on `/fr/application/AP-100482` at seq 74 and found D07.
  - Run 2 (D07 missed) called `page_info` on `/en/`, `/fr/apply`, `/fr/` and `/fr/dashboard`, not on `/fr/application/AP-100482`. It found D04 from an `inspect` on `apply-submit-button` (seq 29).
  - Run 3 (D07 missed) called `page_info` once, on `/fr/` (seq 3). It found D04 from an `inspect` on `apply-submit-button` (seq 73).
- **Category not correct:** the defect was detected, but the finding's category differs from the defect's. Detection does not depend on category for these:
  - default: D03 in runs 1 and 3, A03 in run 2;
  - quick: D03 and A03 in run 1, A04 in runs 2 and 3;
  - opus-low: D03 in run 2;
  - opus-medium: none.

## 3. Clean build

| preset | finding | page | element (testid after conversion) | category / severity | observed (`fr_text`) | scorer class |
|---|---|---|---|---|---|---|
| default | F001 | `/fr/dashboard` | `dashboard-recent-transactions-count` | terminology / low | 3 opérations récentes | known issue U02 |
| default | F002 | `/fr/inexistant` | `heading "Not Found"` (none) | hardcoded_text / low | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| quick | F001 | `/fr/dashboard` | `dashboard-due-date` | date_format / low | 2026-10-01 | unclassified (counted as a false positive) |
| opus-low | F001 | `/fr/dashboard` | `dashboard-recent-transactions-heading` | terminology / low | Transactions récentes | known issue U02 |
| opus-low | F002 | `/fr/inexistant` | `heading "Not Found"` (none) | missing_translation / medium | Not Found — The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| opus-medium | F001 | `/fr/dashboard` | `dashboard-recent-transactions-count` | terminology / low | 3 opérations récentes | known issue U02 |
| opus-medium | F002 | `/fr/apply` | `apply-amount-input` | number_currency_format / medium | 2500,50 → Entrez un montant entre 1 000,00 $ et 50 000,00 $. | known issue U05 |
| opus-medium | F003 | `/fr/inexistant` | `heading "Not Found"` (none) | hardcoded_text / low | Not Found — The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |

| preset | findings | known issue | false positive (control) | unclassified | `false_positive_count` |
|---|---|---|---|---|---|
| default | 2 | 2 (U02, U03) | 0 | 0 | 0 |
| quick | 1 | 0 | 0 | 1 | 1 |
| opus-low | 2 | 2 (U02, U03) | 0 | 0 | 0 |
| opus-medium | 3 | 3 (U02, U03, U05) | 0 | 0 | 0 |

- **Quick F001:** description `The due date and transaction dates are shown in raw ISO format on the French dashboard, unlike the long localized date format used on the application summary page.`, fix "1 octobre 2026 (1er octobre 2026) …". This is the false positive reviewed in `../20261009-plugin-v0.5/comparison.md` § 3: the value is Babel's `fr_CA` short date. The same finding appears in default seeded run 2 (§ 1).
- **U02 findings:** default F001 and opus-medium F001 are on the counter, opus-low F001 on the heading. All three describe "opérations" in the counter against "Transactions" in the heading.
- **Opus-medium F002 (U05):** description `On the French form, an amount typed with the French decimal comma (2500,50), which is within range, is rejected with the out-of-range message, while the equivalent 2500.50 is accepted in English. …`

## 4. Behaviour and cost per run

Sources:

- **Model turns:** the distinct `message.id`s in `_dev/subagent-transcript.jsonl`.
- **Tool calls:** the `tool_use` blocks in those turns; the server's budget count is in parentheses.
- **Screenshots:** the budget count, which equals the `screenshot` entries in `trajectory.jsonl` in every run.
- **Tokens and cost:** the stream log's `result` event, `modelUsage` (one model per run). Cost is `costUSD`, which equals `total_cost_usd` in every run: the CLI's notional figure at list price (`costBasis: list`).
- **Duration:** `run.duration_s`, the server's time from `start_run` to `finish`.

All cache writes are 5-minute writes (the subagent transcripts' `cache_creation` has no 1-hour tokens). Recomputing from the tokens gives exactly `costUSD` in all 16 runs at these per-MTok prices:

- claude-opus-5-5: $4 input, $20 output, $0.20 cache read, $5 cache write.
- claude-sonnet-5-5: $2 input, $10 output, **$0.10** cache read, $2.50 cache write.

05.10 priced Sonnet cache reads at $0.20 (CLI 2.1.295); see § 6.

| preset | run | model turns | tool calls (budget) | screenshots | input | output | thinking | cache read | cache write | duration (s) | cost (USD) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| default | seeded 1 | 20 | 80 (79) | 2 | 40 | 13,255 | 861 | 425,096 | 43,351 | 147.9 | 0.284 |
| default | seeded 2 | 22 | 77 (76) | 4 | 44 | 13,415 | 804 | 523,946 | 48,967 | 134.5 | 0.309 |
| default | seeded 3 | 20 | 74 (73) | 3 | 40 | 12,807 | 945 | 418,409 | 44,402 | 109.1 | 0.281 |
| default | clean | 28 | 72 (70) | 7 | 56 | 7,060 | 879 | 827,409 | 52,708 | 93.6 | 0.285 |
| quick | seeded 1 | 15 | 53 (52) | 0 | 30 | 9,817 | 460 | 221,943 | 24,565 | 116.3 | 0.182 |
| quick | seeded 2 | 16 | 50 (49) | 0 | 32 | 9,389 | 326 | 213,288 | 22,426 | 104.5 | 0.171 |
| quick | seeded 3 | 14 | 43 (42) | 1 | 28 | 8,150 | 364 | 189,018 | 22,840 | 61.3 | 0.158 |
| quick | clean | 14 | 39 (37) | 1 | 28 | 3,710 | 386 | 172,684 | 20,018 | 45.0 | 0.104 |
| opus-low | seeded 1 | 20 | 79 (78) | 1 | 40 | 12,419 | 554 | 404,823 | 40,489 | 142.5 | 0.532 |
| opus-low | seeded 2 | 25 | 75 (74) | 1 | 50 | 12,959 | 476 | 515,820 | 39,227 | 159.6 | 0.559 |
| opus-low | seeded 3 | 21 | 76 (75) | 2 | 42 | 12,209 | 454 | 460,255 | 42,720 | 119.2 | 0.550 |
| opus-low | clean | 27 | 73 (72) | 5 | 54 | 6,767 | 461 | 660,983 | 41,241 | 129.3 | 0.474 |
| opus-medium | seeded 1 | 32 | 101 (100) | 4 | 64 | 16,440 | 1,247 | 969,697 | 51,436 | 215.2 | 0.780 |
| opus-medium | seeded 2 | 32 | 104 (103) | 3 | 64 | 16,779 | 1,026 | 984,697 | 50,713 | 218.8 | 0.786 |
| opus-medium | seeded 3 | 27 | 103 (102) | 3 | 54 | 15,925 | 1,004 | 746,622 | 49,239 | 196.7 | 0.714 |
| opus-medium | clean | 36 | 110 (109) | 5 | 72 | 11,165 | 1,077 | 1,124,233 | 53,627 | 148.5 | 0.717 |

Cost per defect found, per seeded run (cost ÷ scorer recall):

| preset | run 1 | run 2 | run 3 | preset (total cost ÷ total defects found) |
|---|---|---|---|---|
| default | 0.0158 (18) | 0.0163 (19) | 0.0156 (18) | 0.0159 |
| quick | 0.0107 (17) | 0.0107 (16) | 0.0105 (15) | 0.0106 |
| opus-low | 0.0266 (20) | 0.0279 (20) | 0.0275 (20) | 0.0273 |
| opus-medium | 0.0372 (21) | 0.0374 (21) | 0.0340 (21) | 0.0362 |

Seeded runs, mean (min–max):

| | default | quick | opus-low | opus-medium |
|---|---|---|---|---|
| recall | 18.33 (18–19) | 16.00 (15–17) | 20.00 (20–20) | 21.00 (21–21) |
| model turns | 20.7 (20–22) | 15.0 (14–16) | 22.0 (20–25) | 30.3 (27–32) |
| tool calls (transcript) | 77.0 (74–80) | 48.7 (43–53) | 76.7 (75–79) | 102.7 (101–104) |
| tool calls (budget) | 76.0 (73–79) | 47.7 (42–52) | 75.7 (74–78) | 101.7 (100–103) |
| screenshots | 3.0 (2–4) | 0.3 (0–1) | 1.3 (1–2) | 3.3 (3–4) |
| output tokens | 13,159 (12,807–13,415) | 9,119 (8,150–9,817) | 12,529 (12,209–12,959) | 16,381 (15,925–16,779) |
| thinking tokens | 870 (804–945) | 383 (326–460) | 495 (454–554) | 1,092 (1,004–1,247) |
| cache read tokens | 455,817 (418,409–523,946) | 208,083 (189,018–221,943) | 460,299 (404,823–515,820) | 900,339 (746,622–984,697) |
| duration (s) | 130.5 (109.1–147.9) | 94.0 (61.3–116.3) | 140.4 (119.2–159.6) | 210.2 (196.7–218.8) |
| cost (USD) | 0.291 (0.281–0.309) | 0.170 (0.158–0.182) | 0.547 (0.532–0.559) | 0.760 (0.714–0.786) |
| cost per defect found (USD) | 0.0159 | 0.0106 | 0.0273 | 0.0362 |

- No run exhausted its budget (`exhausted` is null). The highest budget count was 109 of 120 tool calls (opus-medium clean).
- Clean build: default $0.285 in 93.6 s, quick $0.104 in 45.0 s, opus-low $0.474 in 129.3 s, opus-medium $0.717 in 148.5 s.

## 5. The four presets side by side

| preset | recall per run | recall mean | seeded precision per run | clean findings | clean false positives | seeded cost mean (USD) | cost per defect found (USD) | seeded duration mean (s) |
|---|---|---|---|---|---|---|---|---|
| default | 18 / 19 / 18 | 18.33 | 1.000 / 0.950 / 1.000 | 2 (U02, U03) | 0 | 0.291 | 0.0159 | 130.5 |
| quick | 17 / 16 / 15 | 16.00 | 1.000 / 1.000 / 1.000 | 1 | 1 (unclassified: ISO due date) | 0.170 | 0.0106 | 94.0 |
| opus-low | 20 / 20 / 20 | 20.00 | 1.000 / 1.000 / 1.000 | 2 (U02, U03) | 0 | 0.547 | 0.0273 | 140.4 |
| opus-medium | 21 / 21 / 21 | 21.00 | 1.000 / 1.000 / 1.000 | 3 (U02, U03, U05) | 0 | 0.760 | 0.0362 | 210.2 |

## 6. Compared with the earlier measurements of the same presets

Earlier measurements:

- **default and quick:** 05.10, the 9 October runs on plugin 0.5.1 (`../20261009-plugin-v0.5/`, `default-20261009-run-1..3`, `quick-20261009-run-1..3`, `clean-default`, `clean-quick`). These are the 05.10 runs with stream logs and clean runs, and the baseline used in `../20261014-plugin-opus55/comparison.md`. The 8 October runs (plugin 0.5.0, no clean runs) scored 18 / 19 / 18 (default) and 16 / 14 / 14 (quick).
- **opus-low:** 05.11, Opus 5.5 effort low, 15 October (`../20261014-plugin-opus55/low-run-1..3`, `low-clean`), with `low-run-3` as re-scored in commit `ba08ae7`.
- **opus-medium:** 05.11, Opus 5.5 effort medium, 16 October morning (`../20261014-plugin-opus55/medium-run-1..3`, `medium-clean`).

The earlier figures are taken from those reports and from 05.10 and 05.11. They were not re-scored here.

What else differs between each pair:

- **default and quick:** plugin 0.5.1 (repo checkout) vs 0.6.0 (`git archive` copy); Claude Code 2.1.295 vs 2.1.301; 9 vs 16 October; runs grouped by preset vs round-robin across presets. `git diff v0.5.1 v0.6.0` changes nothing in `agents/explorer.md`, `agents/explorer-quick.md`, `skills/i18n-explore/` or `skills/i18n-explore-quick/`.
- **opus-low:** 05.11 ran plugin 0.5.3 with a copy of the default agent whose model and effort lines were edited, started by `/i18n-explore` (`run.preset` `default`). These runs used 0.6.0's own `explorer-opus-low` agent and `/i18n-explore-opus-low` skill (`run.preset` `opus-low`). `v0.6.0:agents/explorer-opus-low.md` differs from `v0.5.3:agents/explorer.md` only in the `name`, `description`, `model` and `effort` lines. Claude Code 2.1.301 in both; 15 vs 16 October.
- **opus-medium:** 05.11 ran the uncommitted 0.6.0 working tree; these runs used tag `v0.6.0`. Claude Code 2.1.301 in both; the same day, morning vs afternoon.
- **Sonnet price in the CLI's cost:** the 05.10 costs price Sonnet cache reads at $0.20 per MTok; the 05.13 costs price them at $0.10 (§ 4). The Opus price is the same in 05.11 and 05.13. The "same price" column recomputes the 05.10 runs from their tokens (05.10 runs table) at $0.10; for default this repeats the figures in `../20261014-plugin-opus55/comparison.md` § 5.

| preset | measurement | recall per run | recall mean | cost per run (USD, as reported) | cost mean | cost mean, Sonnet cache read at $0.10 | cost per defect found | duration per run (s) | duration mean (s) | tool calls (budget) mean | screenshots mean | clean: findings / false positives | clean cost (USD) | clean duration (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| default | 05.10 (9 Oct, 0.5.1) | 19 / 18 / 19 | 18.67 | 0.376 / 0.321 / 0.334 | 0.344 | 0.292 (0.317 / 0.277 / 0.283) | 0.0184 (0.0157 at $0.10) | 121.2 / 108.0 / 113.3 | 114.2 | 78.0 | 2.7 | 2 / 1 (ISO due date) | 0.258 (0.213 at $0.10) | 83.3 |
| default | 05.13 (16 Oct, 0.6.0) | 18 / 19 / 18 | 18.33 | 0.284 / 0.309 / 0.281 | 0.291 | 0.291 | 0.0159 | 147.9 / 134.5 / 109.1 | 130.5 | 76.0 | 3.0 | 2 / 0 | 0.285 | 93.6 |
| quick | 05.10 (9 Oct, 0.5.1) | 15 / 15† / 14 | 14.67 | 0.162 / 0.180 / 0.155 | 0.166 | 0.147 (0.145 / 0.159 / 0.137) | 0.0113 (0.0100 at $0.10) | 69.1 / 75.6 / 81.1 | 75.3 | 40.0 | 0 | 3 / 3 (2 if F002 is credited to U04) | 0.111 (0.099 at $0.10) | 43.6 |
| quick | 05.13 (16 Oct, 0.6.0) | 17 / 16 / 15 | 16.00 | 0.182 / 0.171 / 0.158 | 0.170 | 0.170 | 0.0106 | 116.3 / 104.5 / 61.3 | 94.0 | 47.7 | 0.3 | 1 / 1 (ISO due date) | 0.104 | 45.0 |
| opus-low | 05.11 (15 Oct, 0.5.3) | 21 / 21 / 21 | 21.00 | 0.613 / 0.642 / 0.606 | 0.620 | – | 0.0295 | 327.2 / 212.3 / 212.4 | 250.6 | 89.0 | 3.0 | 2 / 0 | 0.439 | 158.8 |
| opus-low | 05.13 (16 Oct, 0.6.0) | 20 / 20 / 20 | 20.00 | 0.532 / 0.559 / 0.550 | 0.547 | – | 0.0273 | 142.5 / 159.6 / 119.2 | 140.4 | 75.7 | 1.3 | 2 / 0 | 0.474 | 129.3 |
| opus-medium | 05.11 (16 Oct am, 0.6.0 tree) | 21 / 21 / 21 | 21.00 | 0.776 / 0.800 / 0.684 | 0.753 | – | 0.0359 | 169.6 / 193.6 / 159.4 | 174.2 | 100.0 | 3.7 | 3 / 0 | 0.620 | 137.4 |
| opus-medium | 05.13 (16 Oct pm, v0.6.0) | 21 / 21 / 21 | 21.00 | 0.780 / 0.786 / 0.714 | 0.760 | – | 0.0362 | 215.2 / 218.8 / 196.7 | 210.2 | 101.7 | 3.3 | 3 / 0 | 0.717 | 148.5 |

† 05.10 quick run 2 has a finding with A01's text and problem filed on `calculator-paylater-checkbox`; credited by hand, the run is 16/21 and the mean 15.00 (`../20261009-plugin-v0.5/comparison.md` § 1).

Per-defect rows that differ between the earlier and the new runs of a preset (found in how many of three runs; earlier → now):

| preset | rows |
|---|---|
| default | G01 3/3 → 2/3 (missed in run 1) |
| quick | D10 3/3 → 2/3; A01 2/3† → 3/3; A02 2/3 → 3/3; A03 0/3 → 1/3; A06 1/3 → 3/3 |
| opus-low | D04 3/3 → 2/3 (missed in run 1); D07 3/3 → 1/3 (missed in runs 2 and 3) |
| opus-medium | none |

Ratios of the means, 05.13 ÷ earlier:

| preset | recall | cost (as reported) | cost (same Sonnet price) | duration |
|---|---|---|---|---|
| default | 0.98 | 0.85 | 1.00 | 1.14 |
| quick | 1.09 | 1.03 | 1.16 | 1.25 |
| opus-low | 0.95 | 0.88 | – | 0.56 |
| opus-medium | 1.00 | 1.01 | – | 1.21 |

- **default:** recall mean 18.33 against 18.67, with the same range (18–19). At the same Sonnet price the mean cost is the same ($0.291 against $0.292); as reported it is $0.291 against $0.344. The duration ranges overlap (109.1–147.9 s against 108.0–121.2 s); the mean is 130.5 s against 114.2 s. The clean run had no false positive (it had one in 05.10), but seeded run 2 reported the same ISO due-date finding.
- **quick:** recall mean 16.00 against 14.67 (15.00 counting the † finding by hand); every new run found A01, A02 and A06, and one found A03, while run 3 missed D10. At the same Sonnet price the mean cost is 1.16 times higher ($0.170 against $0.147); as reported, $0.170 against $0.166. Mean duration 94.0 s against 75.3 s, with overlapping ranges. The clean run had 1 false positive (the ISO due date) against 3.
- **opus-low:** recall 20 in each run against 21 in each run: D04 was missed once and D07 twice. Every new run cost less ($0.532–0.559 against $0.606–0.642) and took less time (119.2–159.6 s against 212.3–327.2 s) than every earlier run. It made fewer tool calls (75.7 against 89.0) and screenshots (1.3 against 3.0). The clean run reported the same two known issues with no false positive.
- **opus-medium:** recall 21 in each run in both measurements, and no per-defect row differs. Mean cost $0.760 against $0.753, with overlapping ranges. Every new run took longer than every earlier run (196.7–218.8 s against 159.4–193.6 s). The clean run reported the same three known issues with no false positive, at $0.717 in 148.5 s against $0.620 in 137.4 s.
