# Scoring report - seeded build

## ai_judge (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 5 | 5 |
| ai | 6 | 0 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | no | 20260923-v2:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | no | 20260923-v2:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20260923-v2:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | no | n/a | - |
| D06 | no | n/a | - |
| D07 | no | n/a | - |
| D08 | no | n/a | - |
| D09 | yes | no | 20260923-v2:/fr/apply#apply-error-fullname |
| D10 | yes | no | 20260923-v2:/fr/dashboard#dashboard-active-loans-count |
| G01 | yes | yes | 20260923-v2:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260923-v2:/fr#landing-cta-apply |
| G04 | yes | yes | 20260923-v2:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260923-v2:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260923-v2:/fr/calculator#calculator-modal-close |
| A03 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20260923-v2:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260923-v2:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260923-v2:/fr#landing-banner-image |
| A07 | yes | no | 20260923-v2:/fr/calculator#calculator-promo-image; 20260923-v2:/fr/calculator#calculator-promo-image |

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

- total cost (USD): 0.419
- total input tokens: 112172
- total output tokens: 14092
- mean duration (s): 164.469
- models: claude-sonnet-5
