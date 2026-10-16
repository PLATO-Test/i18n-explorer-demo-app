# i18n-explorer: Claude Opus 5.5 (effort high, medium and low) vs Claude Sonnet 5.5

This compares four groups. Each has three seeded runs and one clean run, all headless at viewport 1920×1080.

- **Opus 5.5, effort high ("Opus high"):** plugin 0.5.3 with the default agent and preset switched to `claude-opus-5-5`, effort high, run on 14 October. Run setup is in `project/05.11-opus55-experiment.md`.
- **Opus 5.5, effort low ("Opus low"):** the same plugin 0.5.3 copy setup with the default agent and preset set to `claude-opus-5-5`, effort `low`, run on 15 October. Run setup is in `project/05.11-opus55-experiment.md` § "Opus 5.5, effort low". That section lists earlier attempts on the same day (L1, L2, E1, E2, E2b) that were discarded; they are not part of this comparison.
- **Opus 5.5, effort medium ("Opus medium"):** plugin 0.6.0 with its `opus-medium` preset (`/i18n-explore-opus-medium`, agent `explorer-opus-medium`, `claude-opus-5-5`, effort `medium`), run on 16 October.
- **Sonnet 5.5 (effort high):** the plugin 0.5.1 measurement on `claude-sonnet-5-5`, run on 9 October (05.10 group A and C default). Its scores are in `../20261009-plugin-v0.5/` (`default-20261009-run-1..3`, `clean-default`).

The 0.5.0 runs from 8 October are not part of this comparison.

The groups differ in more than the model and effort:

- **Opus low vs Opus high:** effort (`low` vs `high`); Claude Code 2.1.301 vs 2.1.300; date (15 vs 14 October). Plugin version, agent prompt and command are the same.
- **Opus medium vs Opus low and Opus high:**
  - **Effort:** `medium` vs `low` and `high`.
  - **Plugin version: 0.6.0 vs 0.5.3.** 0.6.0 is the working tree of `../i18n-explorer` at version 0.6.0, not yet committed (the repo's latest tag is `v0.5.3`). Compared with tag `v0.5.3`:
    - the medium runs used the plugin's own `explorer-opus-medium` agent, where Opus high and low used 05.11's copy of the default `explorer` agent with the model and effort lines edited. `agents/explorer-opus-medium.md` differs from `v0.5.3:agents/explorer.md` only in the `name`, `description`, `model` and `effort` lines; the instructions are the same.
    - the `i18n-explore-opus-medium` skill differs from `v0.5.3:skills/i18n-explore/SKILL.md` in its name, description and agent, and in passing `--preset opus-medium` in front of the arguments to `start_run`. The `start_run` result the agent saw is the same as in the Opus low runs apart from the run folder.
    - the server changes are: findings schema 1.4.0 (`run.preset` also accepts `opus-low` and `opus-medium`); the `SubagentStop` hook also matches the Opus agents; `report.md` carries a note for the Opus presets.
  - **Claude Code:** 2.1.301 in all four medium runs (`claude_code_version` in each stream log's init event), the same as Opus low; Opus high used 2.1.300.
  - **Date:** 16 October vs 15 and 14 October.
- **Opus (all three) vs Sonnet:**
  - **Plugin version: 0.5.3 (high, low) and 0.6.0 (medium) vs 0.5.1.** `git diff v0.5.1 v0.5.3` in the plugin repo changes no file under `agents/`, `skills/` or `commands/`, apart from the model (and, for Opus low, effort) lines that 05.11 changed in its copy. The server changes are:
    - the origin lock is set after redirects;
    - off-site redirects are refused;
    - the `start_run` message has one more field, `site {origin}`;
    - `run.typed_origin` and `run.effective_origin` were added (findings schema 1.3.0).
  - **Claude Code:** 2.1.300 (Opus high) and 2.1.301 (Opus low, Opus medium) vs 2.1.295.
  - **Date:** 14, 15 and 16 October vs 9 October.
- **MCP connection (05.11):** in the Opus low runs, the plugin's MCP server connected in 4.6 s (run 1), 3.1 s (run 2), 6.7 s (run 3) and 2.5 s (clean); Claude Code logged "version negotiation probe timed out" for runs 1 and 3. Opus high run 2 connected in 3.0 s with no probe message. The connection time was not measured for the Opus medium runs; their init events list the plugin's server as `connected`.

This document does not attribute any difference to any of these factors.

## Inputs

| group | build | run | source | plugin | preset | status | model observed | effort observed | report |
|---|---|---|---|---|---|---|---|---|---|
| Opus high | seeded | 1 | `i18n-explorer/i18n-explorer-runs/20261014-161128-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (43) | high (43) | `run-1/` |
| Opus high | seeded | 2 | `i18n-explorer/i18n-explorer-runs/20261014-161643-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (38) | high (38) | `run-2/` |
| Opus high | seeded | 3 | `i18n-explorer/i18n-explorer-runs/20261014-162158-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (33) | high (33) | `run-3/` |
| Opus high | seeded | all three | the three converted files | | | | | | `stability/` |
| Opus high | clean | 1 | `i18n-explorer/i18n-explorer-runs/20261014-162641-localhost-5001/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (33) | high (33) | `clean/` |
| Opus low | seeded | 1 | `i18n-explorer/i18n-explorer-runs/20261015-182801-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (22) | low (22) | `low-run-1/` |
| Opus low | seeded | 2 | `i18n-explorer/i18n-explorer-runs/20261015-183415-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (24) | low (24) | `low-run-2/` |
| Opus low | seeded | 3 | `i18n-explorer/i18n-explorer-runs/20261015-183839-localhost-5002/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (24) | low (24) | `low-run-3/` |
| Opus low | seeded | all three | the three converted files | | | | | | `low-stability/` |
| Opus low | clean | 1 | `i18n-explorer/i18n-explorer-runs/20261015-184252-localhost-5001/findings.json` | 0.5.3 | default | completed | claude-opus-5-5 (26) | low (26) | `low-clean/` |
| Opus medium | seeded | 1 | `i18n-explorer/i18n-explorer-runs/20261016-095043-localhost-5002/findings.json` | 0.6.0 | opus-medium | completed | claude-opus-5-5 (28) | medium (28) | `medium-run-1/` |
| Opus medium | seeded | 2 | `i18n-explorer/i18n-explorer-runs/20261016-095432-localhost-5002/findings.json` | 0.6.0 | opus-medium | completed | claude-opus-5-5 (33) | medium (33) | `medium-run-2/` |
| Opus medium | seeded | 3 | `i18n-explorer/i18n-explorer-runs/20261016-095815-localhost-5002/findings.json` | 0.6.0 | opus-medium | completed | claude-opus-5-5 (27) | medium (27) | `medium-run-3/` |
| Opus medium | seeded | all three | the three converted files | | | | | | `medium-stability/` |
| Opus medium | clean | 1 | `i18n-explorer/i18n-explorer-runs/20261016-100123-localhost-5001/findings.json` | 0.6.0 | opus-medium | completed | claude-opus-5-5 (32) | medium (32) | `medium-clean/` |
| Sonnet | seeded | 1 | `…\i18n-measure\v051-A-default-1\i18n-explorer-runs\20261009-092740-localhost-5002\findings.json` | 0.5.1 | default | completed | claude-sonnet-5-5 (23) | high (23) | `../20261009-plugin-v0.5/default-20261009-run-1/` |
| Sonnet | seeded | 2 | `…\i18n-measure\v051-A-default-2\i18n-explorer-runs\20261009-093012-localhost-5002\findings.json` | 0.5.1 | default | completed | claude-sonnet-5-5 (19) | high (19) | `../20261009-plugin-v0.5/default-20261009-run-2/` |
| Sonnet | seeded | 3 | `…\i18n-measure\v051-A-default-3\i18n-explorer-runs\20261009-093216-localhost-5002\findings.json` | 0.5.1 | default | completed | claude-sonnet-5-5 (21) | high (21) | `../20261009-plugin-v0.5/default-20261009-run-3/` |
| Sonnet | clean | 1 | `…\i18n-measure\v051-C-default\i18n-explorer-runs\20261009-093920-localhost-5001\findings.json` | 0.5.1 | default | completed | claude-sonnet-5-5 (19) | high (19) | `../20261009-plugin-v0.5/clean-default/` |

The Opus paths are relative to the repo root (`C:\Users\AlexHotvianskyi\dev\ai-multilingual-poc\`). In the Sonnet paths, `…` stands for `C:\Users\AlexHotvianskyi\AppData\Local\Temp`. "Model observed" and "effort observed" are from `run.observed`. The subagent transcripts agree: every Opus high response is `claude-opus-5-5` with `perTurnEffort` `high`, every Opus low response is `claude-opus-5-5` with `perTurnEffort` `low`, and every Sonnet response is `claude-sonnet-5-5` with `perTurnEffort` `high`. For Opus medium, `run.observed` (`agent_type` `i18n-explorer:explorer-opus-medium`) records `claude-opus-5-5` and effort `medium` for every response, and `effort_at_stop` `medium`, in all four runs.

How the Opus runs were scored:

- Each Opus file was converted with `scoring.adapters.plugin_v1` and scored with `scoring.score`. The converted output is kept as `<report>/findings.converted.json`.
- The adapter needed no change for findings schemas 1.3.0 and 1.4.0. They add only the optional `run.typed_origin` and `run.effective_origin`, and two more `run.preset` values, none of which the adapter reads. All twelve converted files passed the scorer's schema check.
- `stability/`, `low-stability/` and `medium-stability/` each score their group's three seeded `findings.converted.json` files together. They were copied into one folder outside the repo for that run.
- **Adapter change (commit `166c917`) and re-scored `low-run-3`:** before the medium runs were scored, the adapter was changed so that an `element` that is exactly an HTML element name (such as `html`) becomes a null testid instead of being taken as one.
  - Re-converting the 22 committed plugin conversions whose source is still on disk with the changed adapter changes one value: `low-run-3` F021, `data_testid` `html` → null.
  - `low-run-3/` and `low-stability/` were converted and scored again; all other Opus high and Opus low reports are unchanged.
  - The four Opus medium files convert byte-identically with the adapter before and after the change, so the medium figures do not depend on it. Their `element` values for D07 are `html lang` (runs 1 and 3, which have a space and were already null) and null (run 2).
- The scorer was not changed. All figures below are the scorer's, except where marked "by hand".

Checks on the inputs and on the baseline:

- The SHA-256 of every Opus high and Opus low source findings.json matched 05.10 or 05.11 before scoring and was unchanged after it. 05.11 records no SHA-256 for the Opus medium runs; their SHA-256 was the same before and after scoring:
  - run 1 `bc8e054ac25777f826b0603bbac23248c5a6ce39dc792cf19e30f98676579865`
  - run 2 `284e31b6cea84f6abdfecdb63f2412c13cf0580dac0042f06b3325dbc223010c`
  - run 3 `3f134a99fe5b43c8d1126bf99b4a3728658be1b1e80bcca42123b6465c562cf8`
  - clean `3e1dadb4a369f9d95eebc07adbd1c8f32928d85ae0e4a873324d35eb48bd4cc1`
- The Sonnet group was not converted again. It was re-scored from its committed `findings.converted.json` files into a scratch folder with the current scorer, and all four `report.json` files equal the committed ones as JSON.

## 1. Recall and precision per run (seeded build)

| group | run | findings | matched a defect | known issue | control false positive | unclassified | recall | precision |
|---|---|---|---|---|---|---|---|---|
| Opus high | `run-1` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus high | `run-2` | 23 | 21 | 2 (U03, U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus high | `run-3` | 22 | 21 | 1 (U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus medium | `medium-run-1` | 22 | 21 | 1 (U03) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus medium | `medium-run-2` | 22 | 21 | 1 (U05) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus medium | `medium-run-3` | 22 | 21 | 1 (U03) | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus low | `low-run-1` | 21 | 21 | 0 | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus low | `low-run-2` | 22 | 22 (two on D07) | 0 | 0 | 0 | 21/21 (1.000) | 1.000 |
| Opus low | `low-run-3` | 21 | 21 | 0 | 0 | 0 | 21/21 (1.000) | 1.000 |
| Sonnet | `default-20261009-run-1` | 20 | 19 | 1 (U03) | 0 | 0 | 19/21 (0.905) | 1.000 |
| Sonnet | `default-20261009-run-2` | 19 | 18 | 1 (U03) | 0 | 0 | 18/21 (0.857) | 1.000 |
| Sonnet | `default-20261009-run-3` | 21 | 19 | 2 (U03, U04) | 0 | 0 | 19/21 (0.905) | 1.000 |

| group | recall min | recall max | recall mean | precision per run |
|---|---|---|---|---|
| Opus high | 21 (1.000) | 21 (1.000) | 21.0 (1.000) | 1.000 / 1.000 / 1.000 |
| Opus medium | 21 (1.000) | 21 (1.000) | 21.0 (1.000) | 1.000 / 1.000 / 1.000 |
| Opus low | 21 (1.000) | 21 (1.000) | 21.0 (1.000) | 1.000 / 1.000 / 1.000 |
| Sonnet | 18 (0.857) | 19 (0.905) | 18.67 (0.889) | 1.000 / 1.000 / 1.000 |

- Precision is matched ÷ (findings − known-issue findings), as the scorer computes it. No run in any group has a control false positive or an unclassified finding. `low-stability/` and `medium-stability/` both give pooled precision and recall of 1.000.
- **`low-run-3`, re-scored:** as committed on 15 October (commit `a484903`), this run scored 20/21 with precision 0.952. Its F021 (`lang_attribute`, `/fr/application/AP-100482`, `element: "html"`, `fr_text` `lang="en"`, `suggested_fix` `lang="fr-CA"`, evidence seq 81) describes D07, but the adapter then took `html` as a testid, so the matcher tried only testid matches and never reached D07's category rule for testid-less findings. With the changed adapter, F021 has no testid and is credited to D07 by that rule. The by-hand figure given on 15 October (21/21, precision 1.000) is now the scorer's.
- **`low-run-2`, two findings on D07:** F014 and F015 are both `lang_attribute` on `/fr/application/AP-100482` with no testid, and both are credited to D07 by its category rule.
  - F014 is a placeholder: `fr_text` "pending verification", `description` "placeholder", evidence seq 38. It was filed at seq 54, before the run's only `page_info` on that page (seq 56).
  - F015 (`fr_text` "en", evidence seq 56) says it supersedes F014. The agent's closing reply says F014 should be deleted; the plugin has no way to withdraw a finding (05.11).
  - The scorer's precision of 1.000 for this run depends on F014 being credited to D07. **By hand,** counting F014 as a false positive would give 21/22 (0.955).
- No other run in any group has two findings on one defect.
- **Known issues in the seeded runs:**
  - U05 (the French apply form rejects amounts typed in fr-CA format) appears in all three Opus high seeded runs and in Opus medium run 2 (F008: `15 000,50 / 15000,50 -> "Entrez un montant entre 1 000,00 $ et 50 000,00 $."`), and in none of the Opus low or Sonnet seeded runs.
  - U03 (the default English 404 page under `/fr/`) appears in Opus medium runs 1 and 3 (F022, `hardcoded_text`, on `/fr/page-inexistante` and `/fr/does-not-exist`: `Not Found — The requested URL was not found on the server. …`), in Opus high runs 1 and 2, and in all three Sonnet runs.
  - Known issues count toward neither recall nor precision.

## 2. Per-defect detection (seeded build)

| id | category | Sonnet 1 | Sonnet 2 | Sonnet 3 | Sonnet | Opus high 1 | Opus high 2 | Opus high 3 | Opus high | Opus medium 1 | Opus medium 2 | Opus medium 3 | Opus medium | Opus low 1 | Opus low 2 | Opus low 3 | Opus low |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | missing_translation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D02 | placeholder | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D03 | hardcoded_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **D04** | truncation | no | no | no | **0/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** |
| D05 | number_currency_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D06 | date_format | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **D07** | lang_attribute | no | no | no | **0/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** |
| D08 | locale_navigation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D09 | untranslated_validation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| D10 | plural | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G01 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G02 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G03 | terminology | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| G04 | register | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A01 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A02 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **A03** | mistranslation | yes | no | yes | **2/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** | yes | yes | yes | **3/3** |
| A04 | mistranslation | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A05 | omission | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A06 | image_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| A07 | image_text | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 | yes | yes | yes | 3/3 |
| **total** | | **19** | **18** | **19** | | **21** | **21** | **21** | | **21** | **21** | **21** | | **21** | **21** | **21** | |

The three rows in bold are the ones where the groups differ: in each, the three Opus groups found the defect in all nine of their runs and Sonnet did not. The other 18 defects were found in all twelve runs. No per-defect row differs between the three Opus groups.

- **A03 in Sonnet run 2:** no finding names `dashboard-statement-link` or "Déclaration mensuelle" (`../20261009-plugin-v0.5/comparison.md` § 2).
- **Category not correct:** the defect was detected, but the finding's category differs from the defect's. Detection does not depend on category for these. Cases:
  - Sonnet: D01 in run 1, and D03 in runs 2 and 3.
  - Opus high: D03 in runs 1 and 3.
  - Opus medium: D03 in run 1 (F002, filed as `missing_translation`) and D01 in run 2 (F017, filed as `hardcoded_text`).
  - Opus low: D03 in run 3 (filed as `missing_translation`).
- **Match by testid:** every defect match in all four groups is by testid except these, which the scorer credits by its other rules:
  - D07 in all three Opus high runs, all three Opus medium runs and all three Opus low runs, by category on the summary page.
  - D08 in Sonnet run 2, by text. Its element, `link "Estimer un nouveau prêt" [testid=dashboard-estimate-loan-link]`, combines a role, a name and a testid, and the adapter turns that form into null.
  - D09 in Opus low run 1, by text. Its element, `Nom complet field error`, is a description rather than a testid, and the adapter turns it into null.

## 3. D04, D07 and A03

### Found or not

| defect | Sonnet 1 | Sonnet 2 | Sonnet 3 | Opus high 1 | Opus high 2 | Opus high 3 | Opus medium 1 | Opus medium 2 | Opus medium 3 | Opus low 1 | Opus low 2 | Opus low 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D04 (`/fr/apply`, `apply-submit-button`) | missed | missed | missed | found (F005) | found (F006) | found (F006) | found (F005) | found (F022) | found (F006) | found (F005) | found (F022) | found (F007) |
| D07 (`/fr/application/AP-100482`, `html lang`) | missed | missed | missed | found (F009) | found (F021) | found (F021) | found (F021) | found (F021) | found (F021) | found (F021) | found (F014, F015) | found (F021) |
| A03 (`/fr/dashboard`, `dashboard-statement-link`) | found (F012) | missed | found (F011) | found (F014) | found (F013) | found (F013) | found (F013) | found (F019) | found (F013) | found (F013) | found (F012) | found (F013) |

### Trajectory, per run

Seq numbers are from each run's `trajectory.jsonl`. "Rows on the page" counts the trajectory entries, other than `report_finding` and `finish`, whose page is the one named. The same count reproduces the Opus high and Opus low figures below.

The Sonnet runs below are reads of the 9 October trajectories, using the same method as `../20261001-sonnet55/comparison.md` and `project/05.3-plugin-vs-poc-scoring.md`.

| defect | run | rows on the page | `read_page` that shows the button / page | screenshot of `/fr/apply` | `inspect` on `apply-submit-button` | `page_info` on the summary page | finding | classification |
|---|---|---|---|---|---|---|---|---|
| D04 | Sonnet 1 | 11, from seq 10 | 11, 13, 20 | none | none | – | none | missed: examined by `read_page` (the label text is correct in both builds); no screenshot of `/fr/apply`; no `inspect` |
| D04 | Sonnet 2 | 17, from seq 14 | 16, 25 | none | none | – | none | missed: same as run 1 |
| D04 | Sonnet 3 | 18, from seq 10 | 11, 13, 20 | none | none | – | none | missed: same as run 1 |
| D04 | Opus high 1 | 30, from seq 11 | 12, 20, 28, 103 | seq 16 | seq 17 | – | F005, evidence `screenshots/016.png`, seq 17 | found |
| D04 | Opus high 2 | 28, from seq 11 | 12, 19, 30, 103 | seq 22 | seq 21 | – | F006, evidence `screenshots/022.png`, seq 22 | found |
| D04 | Opus high 3 | 29, from seq 11 | 12, 19, 32, 101 | seq 23 | seq 21 | – | F006, evidence `screenshots/023.png`, seq 23 | found |
| D04 | Opus medium 1 | 23, from seq 11 | 12, 21, 29 | none | seq 16 | – | F005, evidence seq 17 (the next `inspect`, on `apply-email-label`), filed at seq 18 | found |
| D04 | Opus medium 2 | 28, from seq 11 | 12, 19, 28, 45, 48 | none | seq 98, after a `navigate` back at seq 95 | – | F022, evidence seq 98, filed at seq 101 | found |
| D04 | Opus medium 3 | 22, from seq 12 | 13, 20, 30 | none | seq 22 | – | F006, evidence seq 22, filed at seq 23 | found |
| D04 | Opus low 1 | 20, from seq 11 | 12, 23 | seq 14 | seq 15 | – | F005, evidence `screenshots/014.png`, seq 15 | found |
| D04 | Opus low 2 | 23, from seq 9 | 10, 12, 23 | seq 85 | seq 86 | – | F022, evidence `screenshots/085.png`, seq 86 | found |
| D04 | Opus low 3 | 22, from seq 10 | 11, 13, 21 | seq 35 | seq 36 | – | F007, evidence `screenshots/035.png`, seq 36 | found |
| D07 | Sonnet 1 | 2, entered by `navigate` at seq 40 | 41 | – | – | none | none | missed: reached; no `page_info` call on the page |
| D07 | Sonnet 2 | 2, entered by click at seq 40 | 41 | – | – | none | none | missed: same as run 1 |
| D07 | Sonnet 3 | 2, entered by click at seq 33 | 34 | – | – | none | none | missed: same as run 1 |
| D07 | Opus high 1 | 4, entered by click at seq 44 | 45 | – | – | seq 46 (`html lang: en`) | F009, evidence seq 46 | found |
| D07 | Opus high 2 | 4, entered by click at seq 47 | 48 | – | – | seq 87 (`html lang: en`), after a `navigate` back at seq 86 | F021, evidence seq 87 | found |
| D07 | Opus high 3 | 4, entered by click at seq 48 | 49 | – | – | seq 89 (`html lang: en`), after a `navigate` back at seq 88 | F021, evidence seq 89 | found |
| D07 | Opus medium 1 | 4, entered by click at seq 44 | 45 | – | – | seq 87 (`html lang: en`), after a `navigate` back at seq 86 | F021, evidence seq 87, `element: "html lang"` | found |
| D07 | Opus medium 2 | 4, entered by click at seq 50 | 51 | – | – | seq 94 (`html lang: en`), after a `navigate` back at seq 93 | F021, evidence seq 94, `element` null | found |
| D07 | Opus medium 3 | 4, entered by click at seq 46 | 47 | – | – | seq 84 (`html lang: en`), after a `navigate` back at seq 83 | F021, evidence seq 84, `element: "html lang"` | found |
| D07 | Opus low 1 | 4, entered by click at seq 39 | 40 | – | – | seq 80 (`html lang: en`), after a `navigate` back at seq 79 | F021, evidence seq 80 | found |
| D07 | Opus low 2 | 4, entered by click at seq 37 | 38 | – | – | seq 56 (`html lang: en`), after a `navigate` back at seq 55 | F014 (placeholder, evidence seq 38, filed at seq 54) and F015 (evidence seq 56, filed at seq 57) | found (both findings credited) |
| D07 | Opus low 3 | 4, entered by click at seq 38 | 39 | – | – | seq 81 (`html lang: en`), after a `navigate` back at seq 80 | F021, evidence seq 81, `element: "html"` | found (since the re-score; § 1) |

| defect | run | rows on `/fr/dashboard` | `read_page` that shows the link | finding | classification |
|---|---|---|---|---|---|
| A03 | Sonnet 2 | 2, from seq 47 | 48 (`link "Déclaration mensuelle" [testid=dashboard-statement-link]`) | none | missed: examined by `read_page`, which shows the text; no finding on it |
| A03 | Opus medium 1 | 5, from seq 49 | 50 | F013, evidence seq 50 | found |
| A03 | Opus medium 2 | 5, from seq 78 | 79 | F019, evidence seq 79 | found |
| A03 | Opus medium 3 | 5, from seq 51 | 52 | F013, evidence seq 52 | found |
| A03 | Opus low 1 | 4, from seq 44 | 45 | F013, evidence seq 45 | found |
| A03 | Opus low 2 | 3, from seq 43 | 44 | F012, evidence seq 45 (`page_info`) | found |
| A03 | Opus low 3 | 4, from seq 43 | 44 | F013, evidence seq 44 | found |

The A03 finding evidence in the other runs: Sonnet 1 F012 seq 44, Sonnet 3 F011 seq 39, Opus high F014 seq 52, F013 seq 53 and F013 seq 54.

No run in any group missed D04, D07 or A03 other than the Sonnet runs above, so the trajectory-based classification of misses applies to Sonnet only.

- **Sonnet `page_info` and `inspect` calls:**
  - Every `page_info` call, by run: run 1 at seq 2 (`/fr/`) and seq 82 (`/en/dashboard`); runs 2 and 3 only at seq 2 (`/fr/`).
  - None of the three runs made an `inspect` call.
  - No Sonnet finding contains "Soumettre", "lang=", "html lang", "truncat" or "clipp".
- **Sonnet screenshots:**
  - Run 1: `/en/` and `/fr/calculator`.
  - Run 2: `/en/`, `/en/calculator` and `/fr/calculator`.
  - Run 3: `/en/`, `/fr/calculator` and `/en/calculator`.
- **Opus high `page_info` calls:** each Opus high run called `page_info` on 6 to 8 pages, in both locales. Each also checked the English summary page, except run 3. Every `page_info` call, by run:
  - Run 1: `/fr/`, `/fr/application/AP-100482`, `/fr/calculator`, `/fr/dashboard`, `/en/application/AP-100482`, `/en/dashboard`.
  - Run 2: `/fr/`, `/fr/calculator`, `/fr/application/AP-100482`, `/fr/dashboard`, `/fr/apply`, `/en/application/AP-100482`, `/en/dashboard`, `/en/calculator`.
  - Run 3: `/fr/`, `/fr/calculator`, `/fr/dashboard`, `/fr/application/AP-100482`, `/fr/apply`, `/en/calculator`, `/en/dashboard`.
- **Opus medium `page_info` calls:** 6, 8 and 6. As in Opus low, the `page_info` on the French summary page came after a later return to it, not on the first visit (seq 87, 94 and 84 against first visits at 45, 51 and 47). Every `page_info` call, by run:
  - Run 1: `/fr/`, `/fr/calculator`, `/fr/dashboard`, `/fr/application/AP-100482`, `/fr/apply`, `/en/application/AP-100482`.
  - Run 2: `/fr/`, `/fr/dashboard`, `/fr/calculator`, `/fr/application/AP-100482`, `/fr/apply`, `/en/`, `/en/dashboard`, `/en/calculator`.
  - Run 3: `/fr/`, `/en/`, `/fr/calculator`, `/fr/application/AP-100482`, `/fr/dashboard`, `/fr/apply`.
- **Opus medium screenshots and `inspect`:**
  - Screenshots: run 1 `/fr/`, `/en/calculator`, `/fr/calculator`, `/fr/dashboard`; run 2 `/fr/`, `/en/calculator`, `/fr/calculator`, `/fr/dashboard`; run 3 `/fr/`, `/fr/calculator`, `/fr/dashboard`. No Opus medium run took a screenshot of `/fr/apply`.
  - `inspect` calls: run 1 two, on `apply-submit-button` (seq 16) and `apply-email-label` (seq 17); runs 2 and 3 one each, on `apply-submit-button` (seq 98 and seq 22).
- **Opus low `page_info` calls:** 6 per run. In each run, the `page_info` on the French summary page came after a later return to it, not on the first visit (seq 80, 56 and 81 against first visits at 39, 37 and 38). Every `page_info` call, by run:
  - Run 1: `/fr/`, `/fr/calculator`, `/fr/dashboard`, `/fr/application/AP-100482`, `/en/dashboard`, `/fr/apply`.
  - Run 2: `/en/application/AP-100482`, `/fr/dashboard`, `/fr/application/AP-100482`, `/fr/calculator`, `/fr/`, `/fr/apply`.
  - Run 3: `/fr/`, `/fr/calculator`, `/en/dashboard`, `/fr/dashboard`, `/fr/application/AP-100482`, `/fr/apply`.
- **Opus low screenshots and `inspect`:**
  - Screenshots: run 1 `/fr/`, `/fr/apply`, `/static/img/promo-c.png`; run 2 `/en/`, `/fr/calculator`, `/fr/apply`; run 3 `/fr/`, `/fr/apply`, `/static/img/promo-c.png`.
  - Each run made one `inspect` call, on `apply-submit-button` on `/fr/apply`, directly after its screenshot of that page.
- **Opus D04 findings (all three effort levels):**
  - All nine cite the `inspect` measurement "scrollWidth 290 > clientWidth 210, overflow hidden" (worded differently per run); the Opus high runs, Opus low run 2 and all three Opus medium runs also add "nowrap".
  - Each Opus high and Opus low D04 finding cites both a screenshot of `/fr/apply` and that `inspect` result. The Opus medium D04 findings cite only a trajectory entry, since those runs took no screenshot of the page.
  - In Opus high run 1 and in all three Opus low runs the screenshot came before the `inspect`; in Opus high runs 2 and 3 it came after.

## 4. Clean build

| group | finding | page | element (testid after conversion) | category / severity | observed | scorer class |
|---|---|---|---|---|---|---|
| Opus high | F001 | `/fr/apply` | `apply-amount-input` | number_currency_format / medium | 12500,50 → "Entrez un montant entre 1 000,00 $ et 50 000,00 $." | known issue U05 |
| Opus high | F002 | `/fr/dashboard` | `dashboard-recent-transactions-count` | terminology / low | 3 opérations récentes / Transactions récentes | known issue U02 |
| Opus high | F003 | `/fr/introuvable` | none | hardcoded_text / medium | 404 Not Found / Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Opus medium | F001 | `/fr/apply` | `apply-amount-input` | number_currency_format / medium | 15000,50 / 15 000,50 → "Entrez un montant entre 1 000,00 $ et 50 000,00 $." | known issue U05 |
| Opus medium | F002 | `/fr/dashboard` | `dashboard-recent-transactions-count` | terminology / low | 3 opérations récentes / Transactions récentes | known issue U02 |
| Opus medium | F003 | `/fr/introuvable` | none (`heading "Not Found"`) | missing_translation / medium | Not Found — The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Opus low | F001 | `/fr/dashboard` | `dashboard-recent-transactions-heading` | terminology / low | Transactions récentes | known issue U02 |
| Opus low | F002 | `/fr/nexistepas` | none | hardcoded_text / medium | Not Found — The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Sonnet | F001 | `/fr/nonexistent` | none | hardcoded_text / low | Not Found / The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. | known issue U03 |
| Sonnet | F002 | `/fr/dashboard` | `dashboard-due-date` | date_format / low | 2026-10-01 | unclassified (counted as a false positive) |

| group | findings | known issue | false positive (control) | unclassified | `false_positive_count` |
|---|---|---|---|---|---|
| Opus high | 3 | 3 (U02, U03, U05) | 0 | 0 | 0 |
| Opus medium | 3 | 3 (U02, U03, U05) | 0 | 0 | 0 |
| Opus low | 2 | 2 (U02, U03) | 0 | 0 | 0 |
| Sonnet | 2 | 1 (U03) | 0 | 1 | 1 |

- **Opus high F002 (U02):** the finding's description reads: `The same English term "transactions" is translated as "opérations" in the counter and as "Transactions" in the section heading on the same page; "opérations" is the preferred Quebec banking term.` That is U02 as `known_issues.yaml` describes it.
- **Opus medium F001 (U05):** description: `On the French loan form, amounts typed in Canadian French format (15000,50 or 15 000,50) are rejected as out of range; only the English format 15000.50 is accepted, while the error message itself displays amounts in the French format.` The run typed `15 000,50` (seq 36), `15000,50` (seq 41) and `15000.50` (seq 44) into `apply-amount-input`.
- **Opus medium F002 (U02):** description: `The same English concept "transactions" is rendered as "opérations" in the counter and "Transactions" in the section heading on the same page.` Same element as Opus high F002.
- **Opus medium F003 (U03):** description: `The 404 page under /fr/ is the default English server page with html lang="en", no French text and no site navigation back to the French site.` It is filed as `missing_translation`, where the other groups' U03 findings are `hardcoded_text`; the scorer credits it to U03.
- **Opus low F001 (U02):** the same issue, filed on the heading instead of the counter: `The same concept is called "opérations récentes" in the counter and "Transactions récentes" in the heading; Quebec banking usage prefers "opérations" consistently.`
- **Opus low and U05:** the clean Opus low run has no finding on the apply form's amount format. The values it typed into `apply-amount-input` were `abc` (seq 18 and 23, the latter on `/en/apply`) and `15000` (seq 31); it typed no amount with a decimal comma or a space.
- **Sonnet F002:** a false positive. The value is Babel's `fr_CA` short date. It was reviewed in `../20261009-plugin-v0.5/comparison.md` § 3.

## 5. Behaviour and cost per run

Sources:

- **Model turns:** the distinct `message.id`s in the subagent transcript.
- **Tool calls:** the `tool_use` blocks in those turns. The server's budget counter, in parentheses, is one lower in every run of all four groups.
- **Screenshots:** the `screenshot` calls in `trajectory.jsonl`.
- **Tokens and cost:** the stream log's `result` event, `modelUsage`. Thinking is `thinkingTokens` as `modelUsage` reports it. Cost is `costUSD`, which equals `total_cost_usd` in every run: the CLI's notional figure at list price (`costBasis: list`). For the Opus low and Opus medium runs, recomputing at the Opus 5.5 list prices ($4 input, $20 output, $0.20 cache read, $5 5-minute cache write per MTok) gives exactly `costUSD`.
- **Duration:** `run.duration_s`, the server's time from `start_run` to `finish`.

Cache writes are all 5-minute writes (05.10, 05.11; for Opus medium, the subagent transcripts' `cache_creation` shows only `ephemeral_5m_input_tokens`). The Opus low and Opus medium figures were computed from each run's `_dev/stream.jsonl`, `_dev/subagent-transcript.jsonl` and `trajectory.jsonl`; the same script reproduces the Opus low figures in 05.11.

| group | run | model turns | tool calls (budget) | screenshots | input | output | thinking | cache read | cache write | duration (s) | cost (USD) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sonnet | seeded 1 | 24 | 84 (83) | 2 | 48 | 14,161 | 1,101 | 590,214 | 46,452 | 121.2 | 0.376 |
| Sonnet | seeded 2 | 20 | 79 (78) | 3 | 40 | 13,014 | 788 | 436,068 | 41,258 | 108.0 | 0.321 |
| Sonnet | seeded 3 | 22 | 74 (73) | 3 | 44 | 12,905 | 860 | 514,652 | 40,930 | 113.3 | 0.334 |
| Sonnet | clean | 20 | 70 (69) | 4 | 40 | 7,014 | 890 | 446,877 | 39,231 | 83.3 | 0.258 |
| Opus high | seeded 1 | 44 | 109 (108) | 4 | 88 | 17,177 | 1,567 | 1,435,609 | 59,376 | 271.6 | 0.928 |
| Opus high | seeded 2 | 39 | 110 (109) | 4 | 78 | 17,230 | 1,795 | 1,280,422 | 55,611 | 280.6 | 0.879 |
| Opus high | seeded 3 | 34 | 107 (106) | 4 | 68 | 17,550 | 1,585 | 1,024,463 | 54,006 | 243.2 | 0.826 |
| Opus high | clean | 34 | 98 (97) | 5 | 68 | 10,078 | 1,507 | 1,014,398 | 52,252 | 224.1 | 0.666 |
| Opus medium | seeded 1 | 29 | 100 (99) | 4 | 58 | 16,539 | 1,147 | 815,774 | 56,391 | 169.6 | 0.776 |
| Opus medium | seeded 2 | 34 | 107 (106) | 4 | 68 | 16,269 | 1,223 | 1,020,279 | 53,991 | 193.6 | 0.800 |
| Opus medium | seeded 3 | 28 | 96 (95) | 3 | 56 | 15,010 | 1,007 | 739,414 | 47,209 | 159.4 | 0.684 |
| Opus medium | clean | 33 | 91 (90) | 4 | 66 | 9,761 | 1,428 | 933,713 | 47,479 | 137.4 | 0.620 |
| Opus low | seeded 1 | 23 | 95 (94) | 3 | 46 | 13,903 | 476 | 573,880 | 43,924 | 327.2 | 0.613 |
| Opus low | seeded 2 | 25 | 89 (88) | 3 | 50 | 14,162 | 849 | 655,875 | 45,419 | 212.3 | 0.642 |
| Opus low | seeded 3 | 25 | 86 (85) | 3 | 50 | 13,071 | 618 | 648,684 | 42,917 | 212.4 | 0.606 |
| Opus low | clean | 27 | 70 (69) | 3 | 54 | 6,759 | 563 | 603,351 | 36,638 | 158.8 | 0.439 |

Cost per defect found, per seeded run (cost ÷ scorer recall):

| group | run 1 | run 2 | run 3 | group (total cost ÷ total defects found) |
|---|---|---|---|---|
| Sonnet | 0.0198 (19) | 0.0178 (18) | 0.0176 (19) | 0.0184 |
| Opus high | 0.0442 (21) | 0.0419 (21) | 0.0393 (21) | 0.0418 |
| Opus medium | 0.0370 (21) | 0.0381 (21) | 0.0326 (21) | 0.0359 |
| Opus low | 0.0292 (21) | 0.0306 (21) | 0.0289 (21) | 0.0295 |

Opus low run 3 was 0.0303 (20) before the re-score (§ 1), and the Opus low group figure 0.0300.

Seeded runs, mean (min–max):

| | Sonnet | Opus high | Opus medium | Opus low |
|---|---|---|---|---|
| recall | 18.67 (18–19) | 21.0 (21–21) | 21.0 (21–21) | 21.0 (21–21) |
| model turns | 22 (20–24) | 39 (34–44) | 30.3 (28–34) | 24.3 (23–25) |
| tool calls | 79 (74–84) | 108.7 (107–110) | 101 (96–107) | 90 (86–95) |
| screenshots | 2.7 (2–3) | 4 (4–4) | 3.7 (3–4) | 3 (3–3) |
| output tokens | 13,360 (12,905–14,161) | 17,319 (17,177–17,550) | 15,939 (15,010–16,539) | 13,712 (13,071–14,162) |
| thinking tokens | 916 (788–1,101) | 1,649 (1,567–1,795) | 1,126 (1,007–1,223) | 648 (476–849) |
| cache read tokens | 513,645 (436,068–590,214) | 1,246,831 (1,024,463–1,435,609) | 858,489 (739,414–1,020,279) | 626,146 (573,880–655,875) |
| duration (s) | 114.2 (108.0–121.2) | 265.1 (243.2–280.6) | 174.2 (159.4–193.6) | 250.6 (212.3–327.2) |
| cost (USD) | 0.344 (0.321–0.376) | 0.878 (0.826–0.928) | 0.753 (0.684–0.800) | 0.620 (0.606–0.642) |
| cost per defect found (USD) | 0.0184 | 0.0418 | 0.0359 | 0.0295 |

Ratios of the means:

| | Opus medium ÷ Opus high | Opus medium ÷ Opus low | Opus medium ÷ Sonnet | Opus low ÷ Opus high | Opus low ÷ Sonnet | Opus high ÷ Sonnet |
|---|---|---|---|---|---|---|
| recall | 1.00 | 1.00 | 1.12 | 1.00 | 1.12 | 1.12 |
| model turns | 0.78 | 1.25 | 1.38 | 0.62 | 1.11 | 1.77 |
| tool calls | 0.93 | 1.12 | 1.28 | 0.83 | 1.14 | 1.38 |
| screenshots | 0.92 | 1.22 | 1.38 | 0.75 | 1.12 | 1.50 |
| output tokens | 0.92 | 1.16 | 1.19 | 0.79 | 1.03 | 1.30 |
| thinking tokens | 0.68 | 1.74 | 1.23 | 0.39 | 0.71 | 1.80 |
| cache read tokens | 0.69 | 1.37 | 1.67 | 0.50 | 1.22 | 2.43 |
| duration | 0.66 | 0.70 | 1.53 | 0.95 | 2.20 | 2.32 |
| cost | 0.86 | 1.21 | 2.19 | 0.71 | 1.80 | 2.55 |
| cost per defect found | 0.86 | 1.21 | 1.95 | 0.71 | 1.60 | 2.27 |

The Opus low ratios that use recall changed with the re-score of `low-run-3`: recall vs Opus high 0.98 → 1.00 and vs Sonnet 1.11 → 1.12; cost per defect found vs Opus high 0.72 → 0.71 and vs Sonnet 1.63 → 1.60.

- **Opus medium duration:** every Opus medium run (159.4–193.6 s) was shorter than every Opus high run (243.2–280.6 s) and every Opus low run (212.3–327.2 s), and longer than every Sonnet run (108.0–121.2 s).
- **Opus medium cost:** every Opus medium run ($0.684–0.800) cost less than every Opus high run ($0.826–0.928) and more than every Opus low run ($0.606–0.642).
- **Opus low duration:** runs 2 and 3 (212.3 s and 212.4 s) were shorter than every Opus high run (243.2–280.6 s). Run 1 (327.2 s) was longer than every Opus high run. Every Opus low run was longer than every Sonnet run.
- **Sonnet cache-read price:**
  - The CLI priced Sonnet cache reads at $0.20 per MTok, the figure 05.10 used. 05.11 notes that the current pricing page lists $0.10.
  - At $0.10, the Sonnet seeded costs would be $0.317, $0.277 and $0.283 (mean $0.292, $0.0157 per defect found), and the clean run $0.213.
  - The cost ratios to Sonnet would then be: Opus high 3.00 instead of 2.55; Opus medium 2.58 instead of 2.19 (per defect found 2.29 instead of 1.95); Opus low 2.12 instead of 1.80 (per defect found 1.89 instead of 1.60).
  - The Opus figures do not change: they are already at $0.20, which is 5% of $4.
- **Tool-call budget:** all four groups stayed under the 120 limit. Opus high used 106–109 calls (budget counter), Opus medium 95–106, Opus low 85–94, Sonnet 73–83. No run exhausted the budget (`exhausted` is null).
- **Clean build:** Opus medium cost $0.620 in 137.4 s, Opus low $0.439 in 158.8 s, Opus high $0.666 in 224.1 s, Sonnet $0.258 in 83.3 s.
