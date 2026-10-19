# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 5 | 1 |
| both | 3 | 2 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261019-s5-notset:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261019-s5-notset:/fr#site-footer |
| D04 | yes | yes | 20261019-s5-notset:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261019-s5-notset:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | no | n/a | - |
| G02 | no | n/a | - |
| G03 | yes | yes | 20261019-s5-notset:/fr#landing-cta-apply |
| G04 | yes | yes | 20261019-s5-notset:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | no | 20261019-s5-notset:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261019-s5-notset:/fr#landing-banner-image |
| A07 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-promo-image |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

| known-issue id | count |
|---|---|
| U05 | 1 |

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.762
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.889
- total input tokens: 2399348
- total output tokens: 20602
- mean duration (s): 306.687
- models: claude-sonnet-5
