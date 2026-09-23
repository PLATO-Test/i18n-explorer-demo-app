# Scoring report - seeded build

## deterministic (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 10 | 0 |
| ai | 0 | 6 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | yes | 20260923-v2:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | yes | 20260923-v2:/fr#site-footer; 20260923-v2:/fr#site-footer |
| D04 | yes | yes | 20260923-v2:/fr/apply#apply-submit-button |
| D05 | yes | yes | 20260923-v2:/fr/calculator#calculator-payment-value; 20260923-v2:/fr/calculator#calculator-payment-value |
| D06 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-txn-date-0; 20260923-v2:/fr/dashboard#dashboard-txn-date-1; 20260923-v2:/fr/dashboard#dashboard-txn-date-2 |
| D07 | yes | yes | 20260923-v2:/fr/application/ap-100482#None |
| D08 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-estimate-loan-link |
| D09 | yes | yes | 20260923-v2:/fr/apply#apply-error-fullname; 20260923-v2:/fr/apply#apply-error-fullname; 20260923-v2:/fr/apply#apply-error-fullname |
| D10 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-active-loans-count |
| G01 | yes | yes | 20260923-v2:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260923-v2:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260923-v2:/fr#landing-cta-apply |
| G04 | yes | yes | 20260923-v2:/fr#landing-hero-subtitle |
| A01 | no | n/a | - |
| A02 | no | n/a | - |
| A03 | no | n/a | - |
| A04 | no | n/a | - |
| A05 | no | n/a | - |
| A06 | yes | yes | 20260923-v2:/fr#landing-banner-image |
| A07 | no | n/a | - |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.714
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): n/a
- total input tokens: n/a
- total output tokens: n/a
- mean duration (s): 0.422
- models: n/a
