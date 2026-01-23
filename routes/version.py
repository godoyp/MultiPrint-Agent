from flask import Blueprint, jsonify
from core.config import CONFIG

bp = Blueprint("version", __name__)

@bp.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": CONFIG.get("agent_version", "N/A")
    })
