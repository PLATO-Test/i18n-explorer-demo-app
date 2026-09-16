"""Fixed demo data. No randomness anywhere: every value is a static
fixture so the app renders identically on every run."""
import datetime

ACCOUNT_BALANCE = 12458.30
ACTIVE_LOANS = 0
PENDING_APPLICATIONS = 1
DUE_DATE = datetime.date(2026, 10, 1)
LOAN_RATE = 0.052

# (date, description translation key, amount)
RECENT_TRANSACTIONS = [
    (datetime.date(2026, 9, 15), "dashboard.txn_grocery", -84.12),
    (datetime.date(2026, 9, 12), "dashboard.txn_bill_payment", -145.00),
    (datetime.date(2026, 9, 8), "dashboard.txn_deposit", 2100.00),
]

DEMO_APPLICATION_ID = "AP-100482"

CALCULATOR_DEFAULT_AMOUNT = 15000
CALCULATOR_DEFAULT_TERM = 36

APPLY_AMOUNT_MIN = 1000
APPLY_AMOUNT_MAX = 50000
APPLY_TERM_MIN = 6
APPLY_TERM_MAX = 60
