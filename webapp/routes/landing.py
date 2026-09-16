from flask import Blueprint, g, render_template

bp = Blueprint("landing", __name__, url_prefix="/<any(en, fr):lang>")


@bp.route("/")
def index(lang: str):
    seeded_fr = g.seeded_fr
    banner_file = "banner-en.png" if lang == "en" else "banner-fr.png"
    if seeded_fr:
        banner_file = "banner-en.png"
    html_lang = "fr-CA" if lang == "fr" else "en"
    return render_template(
        "landing.html",
        page_title=g.translator.t("landing.hero_title"),
        html_lang=html_lang,
        banner_file=banner_file,
    )
