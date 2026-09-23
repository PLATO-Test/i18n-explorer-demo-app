# Scoring report - seeded build

## ai_judge (3 runs)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 5 | 5 |
| ai | 6 | 0 |
| both | 4 | 0 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | yes | no | 20260922-final:/fr/dashboard#dashboard-recent-transactions-heading; 20260922-final:/fr/dashboard#dashboard-recent-transactions-heading; 20260922-final:/fr/dashboard#dashboard-recent-transactions-heading |
| D02 | yes | no | 20260922-final:/fr/application/ap-100482#summary-confirmation-message; 20260922-final:/fr/application/ap-100482#summary-confirmation-message; 20260922-final:/fr/application/ap-100482#summary-confirmation-message |
| D03 | yes | no | 20260922-final:/fr#site-footer; 20260922-final:/fr#site-footer; 20260922-final:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | no | n/a | - |
| D06 | no | n/a | - |
| D07 | no | n/a | - |
| D08 | no | n/a | - |
| D09 | yes | no | 20260922-final:/fr/apply#apply-error-fullname; 20260922-final:/fr/apply#apply-error-fullname; 20260922-final:/fr/apply#apply-error-fullname |
| D10 | yes | no | 20260922-final:/fr/dashboard#dashboard-active-loans-count |
| G01 | yes | yes | 20260922-final:/fr/apply#apply-email-label; 20260922-final:/fr/apply#apply-email-label; 20260922-final:/fr/apply#apply-email-label |
| G02 | yes | yes | 20260922-final:/fr/dashboard#dashboard-balance-label; 20260922-final:/fr/dashboard#dashboard-balance-label; 20260922-final:/fr/dashboard#dashboard-balance-label |
| G03 | yes | yes | 20260922-final:/fr#landing-cta-apply; 20260922-final:/fr#landing-cta-apply; 20260922-final:/fr#landing-cta-apply |
| G04 | yes | yes | 20260922-final:/fr#landing-hero-subtitle; 20260922-final:/fr#landing-hero-subtitle; 20260922-final:/fr#landing-hero-subtitle |
| A01 | yes | yes | 20260922-final:/fr/calculator#calculator-paylater-label; 20260922-final:/fr/calculator#calculator-paylater-label; 20260922-final:/fr/calculator#calculator-paylater-label |
| A02 | yes | yes | 20260922-final:/fr/calculator#calculator-modal-close; 20260922-final:/fr/calculator#calculator-modal-close; 20260922-final:/fr/calculator#calculator-modal-close |
| A03 | yes | yes | 20260922-final:/fr/dashboard#dashboard-statement-link; 20260922-final:/fr/dashboard#dashboard-statement-link; 20260922-final:/fr/dashboard#dashboard-statement-link |
| A04 | yes | yes | 20260922-final:/fr/calculator#calculator-early-repayment-note; 20260922-final:/fr/calculator#calculator-early-repayment-note; 20260922-final:/fr/calculator#calculator-early-repayment-note; 20260922-final:/fr/calculator#calculator-early-repayment-note |
| A05 | yes | yes | 20260922-final:/fr/calculator#calculator-rate-note; 20260922-final:/fr/calculator#calculator-rate-note; 20260922-final:/fr/calculator#calculator-rate-note |
| A06 | yes | yes | 20260922-final:/fr#landing-banner-image; 20260922-final:/fr#landing-banner-image; 20260922-final:/fr#landing-banner-image |

### Stability

| id | detected runs | total runs |
|---|---|---|
| A01 | 3 | 3 |
| A02 | 3 | 3 |
| A03 | 3 | 3 |
| A04 | 3 | 3 |
| A05 | 3 | 3 |
| A06 | 3 | 3 |
| D01 | 3 | 3 |
| D02 | 3 | 3 |
| D03 | 3 | 3 |
| D04 | 0 | 3 |
| D05 | 0 | 3 |
| D06 | 0 | 3 |
| D07 | 0 | 3 |
| D08 | 0 | 3 |
| D09 | 3 | 3 |
| D10 | 1 | 3 |
| G01 | 3 | 3 |
| G02 | 3 | 3 |
| G03 | 3 | 3 |
| G04 | 3 | 3 |

### False positives on controls

None.

### Unclassified findings (manual review)

None.

### Precision / recall

- precision: 1.000
- recall: 0.717
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 1.144
- total input tokens: 310903
- total output tokens: 37842
- mean duration (s): 154.703
- models: claude-sonnet-5
