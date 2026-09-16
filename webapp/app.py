from pathlib import Path

from flask import Flask, g, redirect, request, send_from_directory

from webapp.config import build_config
from webapp.i18n import Translator

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"


def create_app(seeded: bool | None = None, app_today: str | None = None) -> Flask:
    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
    app.config.update(build_config(seeded=seeded, app_today=app_today))

    @app.route("/fonts/<path:filename>")
    def fonts(filename):
        # Served directly from the same bundled font used by the banner
        # script, so page text doesn't depend on the host's installed fonts.
        # Explicit mimetype: some hosts' mimetypes module doesn't know
        # .ttf and would otherwise fall back to application/octet-stream.
        return send_from_directory(FONTS_DIR, filename, mimetype="font/ttf")

    from webapp.routes.apply import bp as apply_bp
    from webapp.routes.calculator import bp as calculator_bp
    from webapp.routes.dashboard import bp as dashboard_bp
    from webapp.routes.health import bp as health_bp
    from webapp.routes.landing import bp as landing_bp
    from webapp.routes.summary import bp as summary_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(calculator_bp)
    app.register_blueprint(apply_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(dashboard_bp)

    @app.before_request
    def _set_locale_context() -> None:
        lang = request.view_args.get("lang") if request.view_args else None
        g.locale = lang
        g.seeded = app.config["SEEDED_DEFECTS"]
        g.seeded_fr = g.seeded and lang == "fr"
        if lang is not None:
            g.translator = Translator(lang, g.seeded)

    @app.route("/")
    def root_redirect():
        accept_language = request.headers.get("Accept-Language", "")
        first_tag = accept_language.split(",")[0].strip().lower()
        target = "fr" if first_tag.startswith("fr") else "en"
        return redirect(f"/{target}/")

    @app.context_processor
    def _inject_helpers():
        def t(key: str, **params):
            return g.translator.t(key, **params)

        def alt_url(target_lang: str) -> str:
            path = request.path
            if g.locale and path.startswith(f"/{g.locale}/"):
                new_path = f"/{target_lang}/" + path[len(f"/{g.locale}/"):]
            elif g.locale and path == f"/{g.locale}":
                new_path = f"/{target_lang}"
            else:
                new_path = path
            qs = request.query_string.decode()
            return f"{new_path}?{qs}" if qs else new_path

        return {
            "t": t,
            "locale": g.get("locale"),
            "seeded_fr": g.get("seeded_fr", False),
            "alt_url": alt_url,
            "other_locale": "fr" if g.get("locale") == "en" else "en",
        }

    return app
