# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 6 | 0 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261019-s5-notset:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261019-s5-notset:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-txn-date-0 |
| D07 | yes | yes | 20261019-s5-notset:/fr/application/ap-100482#None |
| D08 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261019-s5-notset:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20261019-s5-notset:/fr/apply#apply-email-label |
| G02 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20261019-s5-notset:/fr#landing-cta-apply |
| G04 | yes | yes | 20261019-s5-notset:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-modal-close |
| A03 | yes | no | 20261019-s5-notset:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261019-s5-notset:/fr#landing-banner-image |
| A07 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-promo-image |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.905
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.834
- total input tokens: 2012930
- total output tokens: 21736
- mean duration (s): 279.469
- models: claude-sonnet-5
