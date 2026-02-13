from flask import Blueprint, send_from_directory


bp = Blueprint("ui", __name__, url_prefix="/ui")

@bp.route("/")
def ui_route():
    return send_from_directory("static", "ui.html")
