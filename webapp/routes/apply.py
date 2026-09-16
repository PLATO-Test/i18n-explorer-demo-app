import re

from flask import Blueprint, g, redirect, render_template, request, session, url_for

from webapp.data.fixtures import (
    APPLY_AMOUNT_MAX,
    APPLY_AMOUNT_MIN,
    APPLY_TERM_MAX,
    APPLY_TERM_MIN,
    DEMO_APPLICATION_ID,
    LOAN_RATE,
)
from webapp.formatting import money

bp = Blueprint("apply", __name__, url_prefix="/<any(en, fr):lang>")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^[0-9()+\-.\s]{7,20}$")


@bp.route("/apply", methods=["GET", "POST"])
def index(lang: str):
    seeded_fr = g.seeded_fr
    t = g.translator.t
    errors: dict[str, str] = {}
    form = {
        "full_name": "",
        "email": "",
        "phone": "",
        "amount": "",
        "term": "",
        "consent": "",
    }

    if request.method == "POST":
        form["full_name"] = request.form.get("full_name", "").strip()
        form["email"] = request.form.get("email", "").strip()
        form["phone"] = request.form.get("phone", "").strip()
        form["amount"] = request.form.get("amount", "").strip()
        form["term"] = request.form.get("term", "").strip()
        form["consent"] = request.form.get("consent", "")

        required_text = t("apply.validation_required")
        if seeded_fr:
            # Field-owner copy-pasted the English string while wiring up
            # this one check and never swapped it for the translation key.
            full_name_required_text = "This field is required."
        else:
            full_name_required_text = required_text

        if not form["full_name"]:
            errors["full_name"] = full_name_required_text
        if not form["email"]:
            errors["email"] = required_text
        elif not _EMAIL_RE.match(form["email"]):
            errors["email"] = t("apply.validation_email_invalid")
        if not form["phone"]:
            errors["phone"] = required_text
        elif not _PHONE_RE.match(form["phone"]):
            errors["phone"] = t("apply.validation_phone_invalid")

        amount_value = None
        if not form["amount"]:
            errors["amount"] = required_text
        else:
            try:
                amount_value = float(form["amount"])
            except ValueError:
                amount_value = None
            if amount_value is None or not (APPLY_AMOUNT_MIN <= amount_value <= APPLY_AMOUNT_MAX):
                errors["amount"] = t(
                    "apply.validation_amount_invalid",
                    min=money(APPLY_AMOUNT_MIN, lang),
                    max=money(APPLY_AMOUNT_MAX, lang),
                )

        term_value = None
        if not form["term"]:
            errors["term"] = required_text
        else:
            try:
                term_value = int(form["term"])
            except ValueError:
                term_value = None
            if term_value is None or not (APPLY_TERM_MIN <= term_value <= APPLY_TERM_MAX):
                errors["term"] = t(
                    "apply.validation_term_invalid",
                    min=APPLY_TERM_MIN,
                    max=APPLY_TERM_MAX,
                )

        if not form["consent"]:
            errors["consent"] = t("apply.validation_consent_required")

        if not errors:
            session["application"] = {
                "full_name": form["full_name"],
                "email": form["email"],
                "amount": amount_value,
                "term": term_value,
                "rate": LOAN_RATE,
            }
            return redirect(url_for("summary.index", lang=lang, app_id=DEMO_APPLICATION_ID))

    return render_template(
        "apply.html",
        page_title=t("apply.title"),
        html_lang="fr-CA" if lang == "fr" else "en",
        form=form,
        errors=errors,
    )
