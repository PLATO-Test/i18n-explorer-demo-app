from flask import Blueprint, current_app, jsonify

bp = Blueprint("health", __name__)


@bp.route("/health")
def health():
    return jsonify(status="ok", build=current_app.config["BUILD_NAME"])
