from flask import Blueprint, request, jsonify
from core.printer_state import set_printer, get_printer
from modules.eventlog import log_event

bp = Blueprint("config", __name__)

@bp.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "printer_name": get_printer()
    })

@bp.route("/config/printer", methods=["POST"])
def set_printer_route():
    data = request.get_json()
    printer = data.get("printer")

    if not printer:
        return jsonify({"error": "Invalid Printer"}), 400

    set_printer(printer)

    log_event(f"SELECTED PRINTER | {printer}")

    return jsonify({
        "status": "ok",
        "printer": printer
    })
