# Scoring report - seeded build

## ai_explorer (6 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 4 | 2 |
| both | 4 | 1 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261008-164325-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261008-164745-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261008-165205-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261009-093437-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261009-093606-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261009-093733-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261008-164325-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261008-164745-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261008-165205-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261009-093437-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261009-093606-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261009-093733-localhost-5002:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261008-164325-localhost-5002:/fr#site-footer; 20261008-164745-localhost-5002:/fr#site-footer; 20261008-165205-localhost-5002:/fr#site-footer; 20261009-093437-localhost-5002:/fr#site-footer; 20261009-093606-localhost-5002:/fr#site-footer; 20261009-093733-localhost-5002:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20261008-164325-localhost-5002:/fr/calculator#calculator-payment-value; 20261008-164745-localhost-5002:/fr/calculator#calculator-payment-value; 20261008-165205-localhost-5002:/fr/calculator#calculator-payment-value; 20261009-093437-localhost-5002:/fr/calculator#calculator-payment-value; 20261009-093606-localhost-5002:/fr/calculator#calculator-payment-value; 20261009-093733-localhost-5002:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261008-164325-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261008-164745-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261008-165205-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261009-093437-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261009-093606-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261009-093733-localhost-5002:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20261008-164325-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261008-164745-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261008-165205-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261009-093437-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261009-093606-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261009-093733-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261008-164325-localhost-5002:/fr/apply#apply-error-fullname; 20261008-164745-localhost-5002:/fr/apply#apply-error-fullname; 20261008-165205-localhost-5002:/fr/apply#apply-error-fullname; 20261009-093437-localhost-5002:/fr/apply#apply-error-fullname; 20261009-093606-localhost-5002:/fr/apply#apply-error-fullname; 20261009-093733-localhost-5002:/fr/apply#apply-error-fullname |
| D10 | yes | yes | 20261008-164325-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261008-165205-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261009-093437-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261009-093606-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261009-093733-localhost-5002:/fr/dashboard#dashboard-active-loans-count |
| G01 | no | n/a | - |
| G02 | yes | yes | 20261008-164325-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261008-164745-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261008-165205-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261009-093437-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261009-093606-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261009-093733-localhost-5002:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20261008-164325-localhost-5002:/fr#landing-cta-apply; 20261008-164745-localhost-5002:/fr#landing-cta-apply; 20261008-165205-localhost-5002:/fr#landing-cta-apply; 20261009-093437-localhost-5002:/fr#landing-cta-apply; 20261009-093606-localhost-5002:/fr#landing-cta-apply; 20261009-093733-localhost-5002:/fr#landing-cta-apply |
| G04 | yes | yes | 20261008-164325-localhost-5002:/fr#landing-hero-subtitle; 20261008-164745-localhost-5002:/fr#landing-hero-subtitle; 20261008-165205-localhost-5002:/fr#landing-hero-subtitle; 20261009-093437-localhost-5002:/fr#landing-hero-subtitle; 20261009-093606-localhost-5002:/fr#landing-hero-subtitle; 20261009-093733-localhost-5002:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261008-164325-localhost-5002:/fr/calculator#calculator-paylater-label; 20261008-164745-localhost-5002:/fr/calculator#calculator-paylater-label; 20261008-165205-localhost-5002:/fr/calculator#calculator-paylater-label; 20261009-093437-localhost-5002:/fr/calculator#calculator-paylater-label; 20261009-093733-localhost-5002:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261008-164325-localhost-5002:/fr/calculator#calculator-modal-close; 20261009-093437-localhost-5002:/fr/calculator#calculator-modal-close; 20261009-093606-localhost-5002:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20261008-164325-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261008-164745-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261009-093437-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261009-093606-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261009-093733-localhost-5002:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261008-164325-localhost-5002:/fr/calculator#calculator-rate-note; 20261008-164745-localhost-5002:/fr/calculator#calculator-rate-note; 20261008-165205-localhost-5002:/fr/calculator#calculator-rate-note; 20261009-093437-localhost-5002:/fr/calculator#calculator-rate-note; 20261009-093606-localhost-5002:/fr/calculator#calculator-rate-note; 20261009-093733-localhost-5002:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261008-164325-localhost-5002:/fr#landing-banner-image; 20261008-164745-localhost-5002:/fr#landing-banner-image; 20261008-165205-localhost-5002:/fr#landing-banner-image; 20261009-093606-localhost-5002:/fr#landing-banner-image |
| A07 | no | n/a | - |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 5 | 6 |
| A02 | 3 | 6 |
| A03 | 0 | 6 |
| A04 | 5 | 6 |
| A05 | 6 | 6 |
| A06 | 4 | 6 |
| A07 | 0 | 6 |
| D01 | 6 | 6 |
| D02 | 6 | 6 |
| D03 | 6 | 6 |
| D04 | 0 | 6 |
| D05 | 6 | 6 |
| D06 | 6 | 6 |
| D07 | 0 | 6 |
| D08 | 6 | 6 |
| D09 | 6 | 6 |
| D10 | 5 | 6 |
| G01 | 0 | 6 |
| G02 | 6 | 6 |
| G03 | 6 | 6 |
| G04 | 6 | 6 |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

| known-issue id | count |
|---|---|
| U04 | 5 |

### Unclassified findings (manual review)

| run | page | testid | observed |
|---|---|---|---|
| 20261009-093606-localhost-5002 | /fr/calculator | calculator-paylater-checkbox | Payer maintenant |

### Precision / recall

- precision: 0.990
- recall: 0.698
- false positive count: 1

### Cost / tokens / duration

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 73.567
- models: claude-sonnet-5-5
