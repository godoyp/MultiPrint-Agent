from flask import Blueprint, jsonify
from multiprint_agent.core.agent_config import get_port, get_version, get_laser_printer, get_thermal_printer
from multiprint_agent.core.agent_state import AGENT_STATE
from multiprint_agent.modules.security.auth import require_session_token


bp = Blueprint("state", __name__)

@bp.route("/state", methods=["GET"])
@require_session_token
def state_route():
    runtime = AGENT_STATE.snapshot()

    return jsonify({
        "status": runtime["status"],
        "current_job_id": runtime["current_job_id"],
        "last_error": runtime["last_error"],
        "printers": {
            "laser": get_laser_printer(),
            "thermal": get_thermal_printer(),
        },
        "port": get_port(),
        "version": get_version()
    })
