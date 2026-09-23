# Scoring report - seeded build

## ai_judge (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 4 | 6 |
| ai | 5 | 1 |
| both | 5 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | no | 20260922-final:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | no | 20260922-final:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20260922-final:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | no | n/a | - |
| D06 | no | n/a | - |
| D07 | no | n/a | - |
| D08 | no | n/a | - |
| D09 | yes | no | 20260922-final:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20260922-final:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260922-final:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260922-final:/fr#landing-cta-apply |
| G04 | yes | yes | 20260922-final:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260922-final:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260922-final:/fr/calculator#calculator-modal-close |
| A03 | yes | yes | 20260922-final:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20260922-final:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260922-final:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260922-final:/fr#landing-banner-image |
| A07 | no | n/a | - |

### False positives on controls

None.

### Known issues (not counted toward recall or false positives)

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.667
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.153
- total input tokens: 58413
- total output tokens: 3399
- mean duration (s): 48.891
- models: claude-sonnet-5
