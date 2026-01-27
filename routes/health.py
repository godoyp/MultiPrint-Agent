from flask import Blueprint, jsonify
from core.printer_state import get_printer
from core.agent_config import AGENT_PORT

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "printer": get_printer(),
        "port": AGENT_PORT
    })
