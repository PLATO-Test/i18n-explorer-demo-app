# Scoring report - seeded build

## ai_explorer (3 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 9 | 1 |
| ai | 6 | 0 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261001-134037-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261001-134259-localhost-5002:/fr/application/ap-100482#summary-confirmation-message; 20261001-134521-localhost-5002:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20261001-134037-localhost-5002:/fr#site-footer; 20261001-134259-localhost-5002:/fr#site-footer; 20261001-134521-localhost-5002:/fr#site-footer |
| D04 | yes | no | 20261001-134037-localhost-5002:/fr/apply#None |
| D05 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-payment-value; 20261001-134259-localhost-5002:/fr/calculator#calculator-payment-value; 20261001-134521-localhost-5002:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-txn-date-0; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261001-134037-localhost-5002:/fr/apply#apply-error-fullname; 20261001-134259-localhost-5002:/fr/apply#apply-error-fullname; 20261001-134521-localhost-5002:/fr/apply#apply-error-fullname |
| D10 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-active-loans-count; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-active-loans-count |
| G01 | yes | yes | 20261001-134037-localhost-5002:/fr/apply#apply-email-label; 20261001-134259-localhost-5002:/fr/apply#apply-email-label; 20261001-134521-localhost-5002:/fr/apply#apply-email-label |
| G02 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-balance-label; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20261001-134037-localhost-5002:/fr#landing-cta-apply; 20261001-134259-localhost-5002:/fr#landing-cta-apply; 20261001-134521-localhost-5002:/fr#landing-cta-apply |
| G04 | yes | yes | 20261001-134037-localhost-5002:/fr#landing-hero-subtitle; 20261001-134259-localhost-5002:/fr#landing-hero-subtitle; 20261001-134521-localhost-5002:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-paylater-label; 20261001-134259-localhost-5002:/fr/calculator#calculator-paylater-label; 20261001-134521-localhost-5002:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-modal-close; 20261001-134259-localhost-5002:/fr/calculator#calculator-modal-close; 20261001-134521-localhost-5002:/fr/calculator#calculator-modal-close |
| A03 | yes | yes | 20261001-134037-localhost-5002:/fr/dashboard#dashboard-statement-link; 20261001-134259-localhost-5002:/fr/dashboard#dashboard-statement-link; 20261001-134521-localhost-5002:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261001-134259-localhost-5002:/fr/calculator#calculator-early-repayment-note; 20261001-134521-localhost-5002:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-rate-note; 20261001-134259-localhost-5002:/fr/calculator#calculator-rate-note; 20261001-134521-localhost-5002:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261001-134037-localhost-5002:/fr#landing-banner-image; 20261001-134259-localhost-5002:/fr#landing-banner-image; 20261001-134521-localhost-5002:/fr#landing-banner-image |
| A07 | yes | yes | 20261001-134037-localhost-5002:/fr/calculator#calculator-promo-image; 20261001-134259-localhost-5002:/fr/calculator#calculator-promo-image; 20261001-134521-localhost-5002:/fr/calculator#calculator-promo-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 3 | 3 |
| A02 | 3 | 3 |
| A03 | 3 | 3 |
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
| D10 | 3 | 3 |
| G01 | 3 | 3 |
| G02 | 3 | 3 |
| G03 | 3 | 3 |
| G04 | 3 | 3 |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

| known-issue id | count |
|---|---|
| U03 | 2 |

### Unclassified findings (manual review)

| run | page | testid | observed |
|---|---|---|---|
| 20261001-134521-localhost-5002 | /fr/nonexistent | None | Not Found / The requested URL was not found on the server. |

### Precision / recall

- precision: 0.983
- recall: 0.921
- false positive count: 1

### Cost / tokens / duration

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 122.333
- models: claude-sonnet-5-5
