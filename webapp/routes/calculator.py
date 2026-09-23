from flask import Blueprint, g, render_template, request

from webapp.data.fixtures import CALCULATOR_DEFAULT_AMOUNT, CALCULATOR_DEFAULT_TERM, LOAN_RATE
from webapp.formatting import money, percent
from webapp.loan import monthly_payment

bp = Blueprint("calculator", __name__, url_prefix="/<any(en, fr):lang>")


def _parse_positive_int(raw: str | None, default: int) -> int:
    try:
        value = int(raw)
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default


@bp.route("/calculator")
def index(lang: str):
    seeded_fr = g.seeded_fr
    amount = _parse_positive_int(request.args.get("amount"), CALCULATOR_DEFAULT_AMOUNT)
    term = _parse_positive_int(request.args.get("term"), CALCULATOR_DEFAULT_TERM)
    pay_later = request.args.get("pay_later") == "on"

    payment = monthly_payment(amount, term, LOAN_RATE)
    payment_locale_override = "en_CA" if seeded_fr else None
    payment_display = money(payment, lang, force_locale=payment_locale_override)
    rate_display = percent(LOAN_RATE, lang)

    if lang == "en":
        promo_file = "promo-a.png"
    else:
        promo_file = "promo-c.png" if seeded_fr else "promo-b.png"

    return render_template(
        "calculator.html",
        page_title=g.translator.t("calculator.title"),
        html_lang="fr-CA" if lang == "fr" else "en",
        amount=amount,
        term=term,
        pay_later=pay_later,
        payment_display=payment_display,
        rate_display=rate_display,
        rate_note_text=g.translator.t("calculator.rate_note", rate=rate_display),
        promo_file=promo_file,
    )
