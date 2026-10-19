# Sonnet 5 explorer, effort level: scoring (2026-10-19)

Eight POC explorer runs (run-ids `20261019-s5-{notset,low,medium,high}`, runs 1 and 2 each) against the seeded build, at commit `1b6b61a` with the effort option described in `project/05.15-sonnet5-effort.md`. Run facts (turns, thinking tokens, cost, duration) come from 05.15 § 7; recall and precision come from the scorer.

## Inputs and method

- Scored files: `inputs/20261019-s5-<level>/findings-ai-explorer-<n>.json`. Their SHA-256 equal the values in 05.15 § 7 for all 8 files, checked before and after scoring.
- Each file was scored with `uv run python -m scoring.score --findings <file> --build seeded --out <level>-run-<n>`, as for `../20260929-poc-control/`. Each level's two files were also scored together (`<level>-stability/`). No adapter, no change to the scorer or to `known_issues.yaml`. All 8 files loaded without a format error.
- The 23 Sep runs 1, 2, 4 and the 29 Sep control runs (A1–A3 at `1b6b61a`, B1–B3 at `0663db9`) were re-scored in memory with `scoring.report.build_report` for per-run rows. Their recall equals `../20260929-poc-control/comparison.md` (23 Sep 19/18/18; A 18/15/16; B 16/17/15).
- Seeded precision is 1.000 in all 8 new runs: 0 control false positives, 0 unclassified. Known-issue hits (not counted): U05 in not set #2 and high #2 (`apply-amount-input`, 1 each). Every other finding matched a different defect.
- The 23 Sep runs had precision 1.000 and one U03 hit each; the 29 Sep runs had precision 1.000 and no known-issue hits.

## 1. Per-run results

| group | run | recall (of 21) | precision | model turns | thinking tokens | cost $ | duration s |
|---|---|---|---|---|---|---|---|
| notset | 1 | 19 (0.905) | 1.000 | 72 | 9,770 | 0.8334 | 279.5 |
| notset | 2 | 16 (0.762) | 1.000 | 81 | 8,020 | 0.8879 | 306.7 |
| low | 1 | 16 (0.762) | 1.000 | 50 | 1,728 | 0.4324 | 163.4 |
| low | 2 | 14 (0.667) | 1.000 | 58 | 1,717 | 0.4706 | 185.1 |
| medium | 1 | 14 (0.667) | 1.000 | 53 | 3,622 | 0.5040 | 213.2 |
| medium | 2 | 17 (0.810) | 1.000 | 64 | 3,747 | 0.6835 | 197.0 |
| high | 1 | 16 (0.762) | 1.000 | 65 | 7,100 | 0.6876 | 242.3 |
| high | 2 | 15 (0.714) | 1.000 | 55 | 5,187 | 0.6934 | 216.9 |
| 23 Sep | 1 | 19 (0.905) | 1.000 | 21 | 1,344 | 0.3147 | 106.4 |
| 23 Sep | 2 | 18 (0.857) | 1.000 | 18 | 801 | 0.2564 | 90.5 |
| 23 Sep | 4 | 18 (0.857) | 1.000 | 19 | 984 | 0.2982 | 126.0 |
| 29 Sep A | 1 | 18 (0.857) | 1.000 | 65 | 7,363 | 0.7510 | 230.9 |
| 29 Sep A | 2 | 15 (0.714) | 1.000 | 65 | 5,659 | 0.6251 | 187.9 |
| 29 Sep A | 3 | 16 (0.762) | 1.000 | 46 | 5,219 | 0.5913 | 237.0 |
| 29 Sep B | 1 | 16 (0.762) | 1.000 | 45 | 6,432 | 0.6171 | 228.3 |
| 29 Sep B | 2 | 17 (0.810) | 1.000 | 60 | 3,672 | 0.6654 | 181.9 |
| 29 Sep B | 3 | 15 (0.714) | 1.000 | 57 | 5,289 | 0.6136 | 213.5 |

## 2. Per-level comparison

| group | recall per run | recall mean (of 21) | precision | model turns per run | model turns mean | thinking tokens mean | cost $ mean | duration s mean |
|---|---|---|---|---|---|---|---|---|
| not set (n=2) | 19 / 16 | 17.5 (0.833) | 1.000 | 72 / 81 | 76.5 | 8,895 | 0.8606 | 293.1 |
| low (n=2) | 16 / 14 | 15.0 (0.714) | 1.000 | 50 / 58 | 54.0 | 1,722 | 0.4515 | 174.3 |
| medium (n=2) | 14 / 17 | 15.5 (0.738) | 1.000 | 53 / 64 | 58.5 | 3,684 | 0.5937 | 205.1 |
| high (n=2) | 16 / 15 | 15.5 (0.738) | 1.000 | 65 / 55 | 60.0 | 6,144 | 0.6905 | 229.6 |
| 23 Sep (n=3, reference) | 19 / 18 / 18 | 18.3 (0.873) | 1.000 | 21 / 18 / 19 | 19.3 | 1,043 | 0.2897 | 107.6 |
| 29 Sep control A (n=3, reference) | 18 / 15 / 16 | 16.3 (0.778) | 1.000 | 65 / 65 / 46 | 58.7 | 6,080 | 0.6558 | 218.6 |
| 29 Sep control B (n=3, reference) | 16 / 17 / 15 | 16.0 (0.762) | 1.000 | 45 / 60 / 57 | 54.0 | 5,131 | 0.6320 | 207.9 |

The two 29 Sep groups pooled (6 runs): recall 15–18, mean 16.2; model turns 45–65; thinking tokens 3,672–7,363; cost $0.5913–0.7510; duration 181.9–237.0 s. The 23 Sep group: model turns 18–21; thinking tokens 801–1,344; cost $0.2564–0.3147; duration 90.5–126.0 s.

## 3. Per-defect rows that differ between levels

Detected / runs. Only rows where the four new levels do not all have the same count are listed.

| id | category | not set | low | medium | high | 23 Sep | 29 Sep A | 29 Sep B |
|---|---|---|---|---|---|---|---|---|
| D04 | truncation | 1/2 | 1/2 | 1/2 | 0/2 | 0/3 | 1/3 | 1/3 |
| D07 | lang_attribute | 1/2 | 1/2 | 0/2 | 1/2 | 0/3 | 0/3 | 1/3 |
| G01 | terminology | 1/2 | 2/2 | 1/2 | 2/2 | 1/3 | 2/3 | 3/3 |
| G03 | terminology | 2/2 | 0/2 | 1/2 | 0/2 | 3/3 | 3/3 | 0/3 |
| A03 | mistranslation | 1/2 | 0/2 | 0/2 | 0/2 | 3/3 | 0/3 | 1/3 |
| A06 | image_text | 2/2 | 0/2 | 1/2 | 1/2 | 3/3 | 3/3 | 1/3 |
| A07 | image_text | 2/2 | 1/2 | 2/2 | 2/2 | 3/3 | 3/3 | 3/3 |
| **total** | | 35/42 | 30/42 | 31/42 | 31/42 | 55/63 | 49/63 | 48/63 |

Same count at all four levels: D01, D02, D03, D05, D06, D08, D09, D10, G02, G04, A01, A02, A04, A05. Of these, G02 is 1/2 and D10 is 0/2 at every level; the rest are 2/2 (D10: 23 Sep 3/3, 29 Sep 0/6).

## 4. Answers

**Does any effort level match the 23 Sep group on recall and on the cost profile?** No.
- Recall: 23 Sep scored 19 / 18 / 18 (mean 18.3). Level means are 17.5 (not set), 15.0 (low), 15.5 (medium), 15.5 (high). One of the 8 runs reaches 18 or more (not set #1, 19). The other seven scored 14–17.
- Cost profile: 23 Sep took 18–21 model turns, 801–1,344 thinking tokens, $0.256–0.315 and 90.5–126.0 s per run. No run at any level falls inside any of these four ranges. Low is nearest: 50 and 58 turns, 1,728 and 1,717 thinking tokens, $0.432 and $0.471, 163.4 and 185.1 s.
- Low also has the lowest recall mean (15.0).

**Does "not set" today match the 29 Sep group?**
- Recall: in range. Not set scored 19 and 16 (mean 17.5); the six 29 Sep runs scored 15–18 (A mean 16.3, B 16.0). The 16 is inside that range. The 19 is above all six 29 Sep runs.
- Cost profile: no. Not set took 72 and 81 model turns (29 Sep: 45–65), 9,770 and 8,020 thinking tokens (3,672–7,363), $0.833 and $0.888 ($0.591–0.751), 279.5 and 306.7 s (181.9–237.0 s). All eight values are above the 29 Sep maximum.
- For comparison, medium (53, 64 turns; 3,622, 3,747 thinking tokens; $0.504, $0.684) and high (65, 55 turns; 7,100, 5,187 tokens; $0.688, $0.693) fall mostly inside the 29 Sep ranges for turns and thinking tokens; low's thinking tokens are below that range.

## 5. Notes

- n=2 per level. Whether the user-settings `effortLevel` reached the CLI under `--setting-sources=` is open in 05.15 § 4. The wire effort was not observed during the 8 runs (05.15 § 6).
- Some detected defects carry `category correct: no` (not set #1 A03; not set #2 A04; low #2 D03; medium #1 D01; high #2 D03 and A04). This is in each `report.md` and does not change recall.
