# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 5 | 1 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20260929-control-A:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20260929-control-A:/fr#site-footer |
| D04 | yes | yes | 20260929-control-A:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20260929-control-A:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20260929-control-A:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20260929-control-A:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260929-control-A:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260929-control-A:/fr#landing-cta-apply |
| G04 | yes | yes | 20260929-control-A:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260929-control-A:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260929-control-A:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20260929-control-A:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260929-control-A:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260929-control-A:/fr#landing-banner-image |
| A07 | yes | yes | 20260929-control-A:/fr/calculator#calculator-promo-image |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.857
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.752
- total input tokens: 1749215
- total output tokens: 19168
- mean duration (s): 230.875
- models: claude-sonnet-5
