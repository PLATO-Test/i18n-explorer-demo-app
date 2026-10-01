# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 4 | 2 |
| both | 4 | 1 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20261001-125644-localhost-5002:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20261001-125644-localhost-5002:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20261001-125644-localhost-5002:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20261001-125644-localhost-5002:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20261001-125644-localhost-5002:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20261001-125644-localhost-5002:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20261001-125644-localhost-5002:/fr/apply#apply-error-fullname |
| D10 | yes | yes | 20261001-125644-localhost-5002:/fr/dashboard#dashboard-active-loans-count |
| G01 | no | n/a | - |
| G02 | yes | yes | 20261001-125644-localhost-5002:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20261001-125644-localhost-5002:/fr#landing-cta-apply |
| G04 | yes | yes | 20261001-125644-localhost-5002:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20261001-125644-localhost-5002:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20261001-125644-localhost-5002:/fr/calculator#calculator-modal-close |
| A03 | no | n/a | - |
| A04 | yes | yes | 20261001-125644-localhost-5002:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20261001-125644-localhost-5002:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20261001-125644-localhost-5002:/fr#landing-banner-image |
| A07 | no | n/a | - |

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

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 75.700
- models: claude-sonnet-5-5
