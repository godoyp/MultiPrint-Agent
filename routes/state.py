from flask import Blueprint, jsonify
from core.agent_config import get_port, get_version, get_laser_printer, get_thermal_printer

bp = Blueprint("state", __name__)

@bp.route("/state", methods=["GET"])
def state_route():
    return jsonify({
        "status": "online",

        # compatibilidade com UI antiga
        "printer_name": get_laser_printer(),

        # novo modelo (UI nova usa isso)
        "printers": {
            "laser": get_laser_printer(),
            "thermal": get_thermal_printer(),
        },

        "port": get_port(),
        "version": get_version()
    })
