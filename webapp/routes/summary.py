from __future__ import annotations

from flask import Blueprint, current_app, g, render_template, session

from webapp.data.fixtures import CALCULATOR_DEFAULT_AMOUNT, CALCULATOR_DEFAULT_TERM, LOAN_RATE
from webapp.formatting import date_long, money, percent

bp = Blueprint("summary", __name__, url_prefix="/<any(en, fr):lang>")


@bp.route("/application/<app_id>")
def index(lang: str, app_id: str):
    seeded_fr = g.seeded_fr
    t = g.translator.t

    application = session.get("application") or {
        "full_name": "",
        "email": "",
        "amount": CALCULATOR_DEFAULT_AMOUNT,
        "term": CALCULATOR_DEFAULT_TERM,
        "rate": LOAN_RATE,
    }

    amount_display = money(application["amount"], lang)
    confirmation_message = t("summary.confirmation_message", amount=amount_display)

    html_lang = "fr-CA" if lang == "fr" else "en"
    if seeded_fr:
        # Regression from an earlier locale-detection rewrite: this page
        # still reads the default html attribute instead of the request locale.
        html_lang = "en"

    return render_template(
        "summary.html",
        page_title=t("summary.title"),
        html_lang=html_lang,
        app_id=app_id,
        confirmation_message=confirmation_message,
        amount_display=amount_display,
        term=application["term"],
        rate_display=percent(application["rate"], lang),
        submitted_date_display=date_long(current_app.config["APP_TODAY"], lang),
    )
