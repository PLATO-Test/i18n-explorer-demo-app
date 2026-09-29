# Scoring report - clean build

## ai_explorer (1 run)

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

| known-issue id | count |
|---|---|
| U03 | 1 |

### Unclassified findings (manual review)

| run | page | testid | observed |
|---|---|---|---|
| 20260928-161934-localhost-5001 | /fr/dashboard | dashboard-active-loans-count | 0 prêt actif |
| 20260928-161934-localhost-5001 | /fr/apply | apply-amount-input | Entrez un montant entre 1 000,00 $ et 50 000,00 $. (shown when amount="15 000,50") |

### Precision / recall

- precision: n/a
- recall: n/a
- false positive count: 2

### Cost / tokens / duration

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 284.700
- models: claude-sonnet-5
