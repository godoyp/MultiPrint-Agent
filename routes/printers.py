import win32print
from flask import Blueprint, request, jsonify
from core.agent_config import set_printer
from modules.eventlog import log_event

bp = Blueprint("printers", __name__)

@bp.route("/printers", methods=["GET"])
def list_printers():
    printers = [p[2] for p in win32print.EnumPrinters(2)]
    log_event("PRINTER LIST UPDATED")
    return jsonify(printers)


@bp.route("/printer", methods=["PUT"])
def select_printer():
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
