from flask import Blueprint, jsonify
from core.agent_config import get_port, get_version, get_printer

bp = Blueprint("state", __name__)

@bp.route("/state", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "printer_name": get_printer(),
        "port": get_port(),
        "version": get_version()
    })
