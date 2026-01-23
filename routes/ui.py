from flask import Blueprint, send_from_directory

bp = Blueprint("ui", __name__)

@bp.route("/ui")
def ui():
    return send_from_directory("static", "ui.html")
