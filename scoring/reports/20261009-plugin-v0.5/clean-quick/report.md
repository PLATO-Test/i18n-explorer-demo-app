# Scoring report - clean build

## ai_explorer (1 run)

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

| run | page | testid | observed |
|---|---|---|---|
| 20261009-094056-localhost-5001 | /fr/calculator | calculator-early-repayment-note | Aucuns frais ne s'appliquent au remboursement anticipé. |
| 20261009-094056-localhost-5001 | /fr/calculator | None | Calculateur de prêt |
| 20261009-094056-localhost-5001 | /fr/dashboard | dashboard-due-date | 2026-10-01 |

### Precision / recall

- precision: n/a
- recall: n/a
- false positive count: 3

### Cost / tokens / duration

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 43.600
- models: claude-sonnet-5-5
