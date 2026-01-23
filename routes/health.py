from flask import Blueprint, jsonify
from core.printer_state import get_printer
from core.config import PORT

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "printer": get_printer(),
        "port": PORT
    })
