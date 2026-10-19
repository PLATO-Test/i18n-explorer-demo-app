# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 7 | 3 |
| ai | 5 | 1 |
| both | 2 | 3 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | no | 20261019-s5-medium:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261019-s5-medium:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261019-s5-medium:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261019-s5-medium:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20261019-s5-medium:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261019-s5-medium:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20261019-s5-medium:/fr/apply#apply-email-label |
| G02 | no | n/a | - |
| G03 | no | n/a | - |
| G04 | yes | yes | 20261019-s5-medium:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-rate-note |
| A06 | no | n/a | - |
| A07 | yes | yes | 20261019-s5-medium:/fr/calculator#calculator-promo-image |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.667
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.505
- total input tokens: 1100293
- total output tokens: 13312
- mean duration (s): 213.203
- models: claude-sonnet-5
