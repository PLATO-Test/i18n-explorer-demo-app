# Scoring report - seeded build

## ai_explorer (3 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 9 | 1 |
| ai | 6 | 0 |
| both | 4 | 1 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20260929-control-B:/fr/dashboard#dashboard-recent-transactions-heading; 20260929-control-B:/fr/dashboard#dashboard-recent-transactions-heading; 20260929-control-B:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20260929-control-B:/fr/application/ap-100482#summary-confirmation-message; 20260929-control-B:/fr/application/ap-100482#summary-confirmation-message; 20260929-control-B:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20260929-control-B:/fr#site-footer; 20260929-control-B:/fr#site-footer; 20260929-control-B:/fr#site-footer |
| D04 | yes | yes | 20260929-control-B:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20260929-control-B:/fr/calculator#calculator-payment-value; 20260929-control-B:/fr/calculator#calculator-payment-value; 20260929-control-B:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20260929-control-B:/fr/dashboard#dashboard-txn-date-0; 20260929-control-B:/fr/dashboard#dashboard-txn-date-0; 20260929-control-B:/fr/dashboard#dashboard-txn-date-0 |
| D07 | yes | yes | 20260929-control-B:/fr/application/ap-100482#None |
| D08 | yes | yes | 20260929-control-B:/fr/dashboard#dashboard-estimate-loan-link; 20260929-control-B:/fr/dashboard#dashboard-estimate-loan-link; 20260929-control-B:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20260929-control-B:/fr/apply#apply-error-fullname; 20260929-control-B:/fr/apply#apply-error-fullname; 20260929-control-B:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20260929-control-B:/fr/apply#apply-email-label; 20260929-control-B:/fr/apply#apply-email-label; 20260929-control-B:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260929-control-B:/fr/dashboard#dashboard-balance-label; 20260929-control-B:/fr/dashboard#dashboard-balance-label |
| G03 | no | n/a | - |
| G04 | yes | yes | 20260929-control-B:/fr#landing-hero-subtitle; 20260929-control-B:/fr#landing-hero-subtitle; 20260929-control-B:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260929-control-B:/fr/calculator#calculator-paylater-label; 20260929-control-B:/fr/calculator#calculator-paylater-label; 20260929-control-B:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260929-control-B:/fr/calculator#calculator-modal-close; 20260929-control-B:/fr/calculator#calculator-modal-close; 20260929-control-B:/fr/calculator#calculator-modal-close |
| A03 | yes | no | 20260929-control-B:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20260929-control-B:/fr/calculator#calculator-early-repayment-note; 20260929-control-B:/fr/calculator#calculator-early-repayment-note; 20260929-control-B:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260929-control-B:/fr/calculator#calculator-rate-note; 20260929-control-B:/fr/calculator#calculator-rate-note; 20260929-control-B:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260929-control-B:/fr#landing-banner-image |
| A07 | yes | yes | 20260929-control-B:/fr/calculator#calculator-promo-image; 20260929-control-B:/fr/calculator#calculator-promo-image; 20260929-control-B:/fr/calculator#calculator-promo-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 3 | 3 |
| A02 | 3 | 3 |
| A03 | 1 | 3 |
| A04 | 3 | 3 |
| A05 | 3 | 3 |
| A06 | 1 | 3 |
| A07 | 3 | 3 |
| D01 | 3 | 3 |
| D02 | 3 | 3 |
| D03 | 3 | 3 |
| D04 | 1 | 3 |
| D05 | 3 | 3 |
| D06 | 3 | 3 |
| D07 | 1 | 3 |
| D08 | 3 | 3 |
| D09 | 3 | 3 |
| D10 | 0 | 3 |
| G01 | 3 | 3 |
| G02 | 2 | 3 |
| G03 | 0 | 3 |
| G04 | 3 | 3 |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.762
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 1.899
- total input tokens: 4367967
- total output tokens: 49406
- mean duration (s): 207.911
- models: claude-sonnet-5
