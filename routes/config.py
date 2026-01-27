import json
from flask import Blueprint, request, jsonify
from core.agent_config import CONFIG
from core.printer_state import set_printer
from modules.eventlog import log_event

bp = Blueprint("config", __name__)

@bp.route("/config", methods=["GET"])
def get_config():
    return jsonify(CONFIG)


@bp.route("/config/printer", methods=["POST"])
def set_printer_route():
    data = request.get_json()
    printer = data.get("printer")

    if not printer:
        return jsonify({"error": "Invalid Printer"}), 400

    set_printer(printer)

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=2, ensure_ascii=False)

    log_event(f"SELECTED PRINTER | {printer}")

    return jsonify({"status": "ok", "printer": printer})
