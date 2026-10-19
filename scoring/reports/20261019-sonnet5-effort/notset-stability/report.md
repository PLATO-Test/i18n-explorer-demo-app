# Scoring report - seeded build

## ai_explorer (2 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 9 | 1 |
| ai | 6 | 0 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-recent-transactions-heading; 20261019-s5-notset:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261019-s5-notset:/fr/application/ap-100482#summary-confirmation-message; 20261019-s5-notset:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261019-s5-notset:/fr#site-footer; 20261019-s5-notset:/fr#site-footer |
| D04 | yes | yes | 20261019-s5-notset:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-payment-value; 20261019-s5-notset:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-txn-date-0; 20261019-s5-notset:/fr/dashboard#dashboard-txn-date-0 |
| D07 | yes | yes | 20261019-s5-notset:/fr/application/ap-100482#None |
| D08 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-estimate-loan-link; 20261019-s5-notset:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261019-s5-notset:/fr/apply#apply-error-fullname; 20261019-s5-notset:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20261019-s5-notset:/fr/apply#apply-email-label |
| G02 | yes | yes | 20261019-s5-notset:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20261019-s5-notset:/fr#landing-cta-apply; 20261019-s5-notset:/fr#landing-cta-apply |
| G04 | yes | yes | 20261019-s5-notset:/fr#landing-hero-subtitle; 20261019-s5-notset:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-paylater-label; 20261019-s5-notset:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-modal-close; 20261019-s5-notset:/fr/calculator#calculator-modal-close |
| A03 | yes | no | 20261019-s5-notset:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-early-repayment-note; 20261019-s5-notset:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-rate-note; 20261019-s5-notset:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261019-s5-notset:/fr#landing-banner-image; 20261019-s5-notset:/fr#landing-banner-image |
| A07 | yes | yes | 20261019-s5-notset:/fr/calculator#calculator-promo-image; 20261019-s5-notset:/fr/calculator#calculator-promo-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 2 | 2 |
| A02 | 2 | 2 |
| A03 | 1 | 2 |
| A04 | 2 | 2 |
| A05 | 2 | 2 |
| A06 | 2 | 2 |
| A07 | 2 | 2 |
| D01 | 2 | 2 |
| D02 | 2 | 2 |
| D03 | 2 | 2 |
| D04 | 1 | 2 |
| D05 | 2 | 2 |
| D06 | 2 | 2 |
| D07 | 1 | 2 |
| D08 | 2 | 2 |
| D09 | 2 | 2 |
| D10 | 0 | 2 |
| G01 | 1 | 2 |
| G02 | 1 | 2 |
| G03 | 2 | 2 |
| G04 | 2 | 2 |

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
- recall: 0.833
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 1.723
- total input tokens: 4412278
- total output tokens: 42338
- mean duration (s): 293.078
- models: claude-sonnet-5
