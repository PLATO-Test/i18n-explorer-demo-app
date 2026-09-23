# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 8 | 2 |
| ai | 6 | 0 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20260923-v2:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20260923-v2:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | yes | yes | 20260923-v2:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-txn-date-0 |
| D07 | no | n/a | - |
| D08 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20260923-v2:/fr/apply#apply-error-fullname |
| D10 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-active-loans-count |
| G01 | yes | yes | 20260923-v2:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260923-v2:/fr#landing-cta-apply |
| G04 | yes | yes | 20260923-v2:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260923-v2:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260923-v2:/fr/calculator#None |
| A03 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20260923-v2:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260923-v2:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260923-v2:/fr#landing-banner-image |
| A07 | yes | yes | 20260923-v2:/fr/calculator#calculator-promo-image |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

| known-issue id | count |
|---|---|
| U03 | 1 |

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.905
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.316
- total input tokens: 420674
- total output tokens: 10290
- mean duration (s): 106.391
- models: claude-sonnet-5
