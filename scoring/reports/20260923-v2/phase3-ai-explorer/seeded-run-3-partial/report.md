# Scoring report - seeded build

## ai_explorer (1 run)

### Detected / missed by expected layer

| layer | detected | missed |
|---|---|---|
| deterministic | 2 | 8 |
| ai | 0 | 6 |
| both | 4 | 1 |

### Per-defect

| id | detected | category correct | matched findings |
|---|---|---|---|
| D01 | no | n/a | - |
| D02 | no | n/a | - |
| D03 | yes | no | 20260923-v2:/fr#site-footer |
| D04 | no | n/a | - |
| D05 | no | n/a | - |
| D06 | no | n/a | - |
| D07 | no | n/a | - |
| D08 | no | n/a | - |
| D09 | yes | yes | 20260923-v2:/fr/apply#apply-error-fullname |
| D10 | no | n/a | - |
| G01 | yes | yes | 20260923-v2:/fr/apply#apply-email-label |
| G02 | no | n/a | - |
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
- recall: 0.286
- false positive count: 0

### Cost / tokens / duration

- total cost (USD): 0.082
- total input tokens: 58532
- total output tokens: 3300
- mean duration (s): 34.812
- models: claude-sonnet-5
