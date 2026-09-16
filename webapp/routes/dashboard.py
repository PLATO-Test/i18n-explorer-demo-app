from flask import Blueprint, g, render_template, url_for

from webapp.data.fixtures import (
    ACCOUNT_BALANCE,
    ACTIVE_LOANS,
    DUE_DATE,
    PENDING_APPLICATIONS,
    RECENT_TRANSACTIONS,
)
from webapp.formatting import date_short, money

bp = Blueprint("dashboard", __name__, url_prefix="/<any(en, fr):lang>")


@bp.route("/dashboard")
def index(lang: str):
    seeded_fr = g.seeded_fr
    t = g.translator.t

    # D10: the active-loan counter should always follow the CLDR plural
    # rule of the page's own locale. Seeded fr build reuses the English
    # rule here, a plausible copy-paste from an earlier English-only build.
    active_loans_plural_locale = "en" if seeded_fr else lang

    transactions = [
        {
            "date": date_short(txn_date, lang, force_mmddyyyy=seeded_fr),
            "description": t(desc_key),
            "amount": money(amount, lang),
        }
        for txn_date, desc_key, amount in RECENT_TRANSACTIONS
    ]

    estimate_loan_lang = "en" if seeded_fr else lang

    return render_template(
        "dashboard.html",
        page_title=t("dashboard.title"),
        html_lang="fr-CA" if lang == "fr" else "en",
        balance_display=money(ACCOUNT_BALANCE, lang),
        active_loans_text=t("dashboard.active_loans", count=ACTIVE_LOANS, plural_locale=active_loans_plural_locale),
        pending_applications_text=t("dashboard.pending_applications", count=PENDING_APPLICATIONS),
        recent_transactions_count_text=t("dashboard.recent_transactions_count", count=len(RECENT_TRANSACTIONS)),
        transactions=transactions,
        due_date_display=date_short(DUE_DATE, lang),
        estimate_loan_url=url_for("calculator.index", lang=estimate_loan_lang),
    )
