from flask import Blueprint, send_from_directory
from multiprint_web_agent.core.paths import STATIC_DIR


bp = Blueprint("ui", __name__, url_prefix="/ui")

@bp.route("/")
def ui_route():
    return send_from_directory(STATIC_DIR, "ui.html")
