# Scoring report - seeded build

## ai_explorer (2 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 5 | 1 |
| both | 4 | 1 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261019-s5-high:/fr/dashboard#dashboard-recent-transactions-heading; 20261019-s5-high:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261019-s5-high:/fr/application/ap-100482#summary-confirmation-message; 20261019-s5-high:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261019-s5-high:/fr#site-footer; 20261019-s5-high:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-payment-value; 20261019-s5-high:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261019-s5-high:/fr/dashboard#dashboard-txn-date-0; 20261019-s5-high:/fr/dashboard#dashboard-txn-date-0 |
| D07 | yes | yes | 20261019-s5-high:/fr/application/ap-100482#None |
| D08 | yes | yes | 20261019-s5-high:/fr/dashboard#dashboard-estimate-loan-link; 20261019-s5-high:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261019-s5-high:/fr/apply#apply-error-fullname; 20261019-s5-high:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20261019-s5-high:/fr/apply#apply-email-label; 20261019-s5-high:/fr/apply#apply-email-label |
| G02 | yes | yes | 20261019-s5-high:/fr/dashboard#dashboard-balance-label |
| G03 | no | n/a | - |
| G04 | yes | yes | 20261019-s5-high:/fr#landing-hero-subtitle; 20261019-s5-high:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-paylater-label; 20261019-s5-high:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-modal-close; 20261019-s5-high:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-early-repayment-note; 20261019-s5-high:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-rate-note; 20261019-s5-high:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261019-s5-high:/fr#landing-banner-image |
| A07 | yes | yes | 20261019-s5-high:/fr/calculator#calculator-promo-image; 20261019-s5-high:/fr/calculator#calculator-promo-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 2 | 2 |
| A02 | 2 | 2 |
| A03 | 0 | 2 |
| A04 | 2 | 2 |
| A05 | 2 | 2 |
| A06 | 1 | 2 |
| A07 | 2 | 2 |
| D01 | 2 | 2 |
| D02 | 2 | 2 |
| D03 | 2 | 2 |
| D04 | 0 | 2 |
| D05 | 2 | 2 |
| D06 | 2 | 2 |
| D07 | 1 | 2 |
| D08 | 2 | 2 |
| D09 | 2 | 2 |
| D10 | 0 | 2 |
| G01 | 2 | 2 |
| G02 | 1 | 2 |
| G03 | 0 | 2 |
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
- recall: 0.738
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 1.383
- total input tokens: 3271978
- total output tokens: 35657
- mean duration (s): 229.617
- models: claude-sonnet-5
