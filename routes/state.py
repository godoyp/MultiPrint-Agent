from flask import Blueprint, jsonify
from core.agent_config import get_port, get_version, get_laser_printer, get_thermal_printer

bp = Blueprint("state", __name__)

@bp.route("/state", methods=["GET"])
def state_route():
    return jsonify({
        "status": "online",
        
        "printers": {
            "laser": get_laser_printer(),
            "thermal": get_thermal_printer(),
        },

        "port": get_port(),
        "version": get_version()
    })
