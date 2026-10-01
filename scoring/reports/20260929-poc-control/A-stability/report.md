# Scoring report - seeded build

## ai_explorer (3 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 5 | 1 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-recent-transactions-heading; 20260929-control-A:/fr/dashboard#dashboard-recent-transactions-heading; 20260929-control-A:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20260929-control-A:/fr/application/ap-100482#summary-confirmation-message; 20260929-control-A:/fr/application/ap-100482#summary-confirmation-message; 20260929-control-A:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20260929-control-A:/fr#site-footer; 20260929-control-A:/fr#site-footer; 20260929-control-A:/fr#site-footer |
| D04 | yes | yes | 20260929-control-A:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20260929-control-A:/fr/calculator#calculator-payment-value; 20260929-control-A:/fr/calculator#calculator-payment-value; 20260929-control-A:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-txn-date-0; 20260929-control-A:/fr/dashboard#dashboard-txn-date-0; 20260929-control-A:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-estimate-loan-link; 20260929-control-A:/fr/dashboard#dashboard-estimate-loan-link; 20260929-control-A:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20260929-control-A:/fr/apply#apply-error-fullname; 20260929-control-A:/fr/apply#apply-error-fullname; 20260929-control-A:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20260929-control-A:/fr/apply#apply-email-label; 20260929-control-A:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260929-control-A:/fr#landing-cta-apply; 20260929-control-A:/fr#landing-cta-apply; 20260929-control-A:/fr#landing-cta-apply |
| G04 | yes | yes | 20260929-control-A:/fr#landing-hero-subtitle; 20260929-control-A:/fr#landing-hero-subtitle; 20260929-control-A:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260929-control-A:/fr/calculator#calculator-paylater-label; 20260929-control-A:/fr/calculator#calculator-paylater-label; 20260929-control-A:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260929-control-A:/fr/calculator#calculator-modal-close; 20260929-control-A:/fr/calculator#calculator-modal-close; 20260929-control-A:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20260929-control-A:/fr/calculator#calculator-early-repayment-note; 20260929-control-A:/fr/calculator#calculator-early-repayment-note; 20260929-control-A:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260929-control-A:/fr/calculator#calculator-rate-note; 20260929-control-A:/fr/calculator#calculator-rate-note; 20260929-control-A:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260929-control-A:/fr#landing-banner-image; 20260929-control-A:/fr#landing-banner-image; 20260929-control-A:/fr#landing-banner-image |
| A07 | yes | yes | 20260929-control-A:/fr/calculator#calculator-promo-image; 20260929-control-A:/fr/calculator#calculator-promo-image; 20260929-control-A:/fr/calculator#calculator-promo-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 3 | 3 |
| A02 | 3 | 3 |
| A03 | 0 | 3 |
| A04 | 3 | 3 |
| A05 | 3 | 3 |
| A06 | 3 | 3 |
| A07 | 3 | 3 |
| D01 | 3 | 3 |
| D02 | 3 | 3 |
| D03 | 3 | 3 |
| D04 | 1 | 3 |
| D05 | 3 | 3 |
| D06 | 3 | 3 |
| D07 | 0 | 3 |
| D08 | 3 | 3 |
| D09 | 3 | 3 |
| D10 | 0 | 3 |
| G01 | 2 | 3 |
| G02 | 1 | 3 |
| G03 | 3 | 3 |
| G04 | 3 | 3 |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.778
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 1.970
- total input tokens: 4516347
- total output tokens: 51382
- mean duration (s): 218.594
- models: claude-sonnet-5
