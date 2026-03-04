import win32print
from flask import Blueprint, request, jsonify, abort
from multiprint_web_agent.core.agent_config import set_printer
from multiprint_web_agent.modules.observability.eventlog import log_event
from multiprint_web_agent.modules.security.auth import require_session_token
from multiprint_web_agent.modules.printers.detector import is_zebra_printer


bp = Blueprint("printers", __name__)

@bp.route("/printers", methods=["GET"])
@require_session_token
def list_printers_route():
    printers = [p[2] for p in win32print.EnumPrinters(2)]
    log_event("PRINTER LIST UPDATED")
    return jsonify(printers)

@bp.route("/printers/classified", methods=["GET"])
@require_session_token
def list_printers_classified_route():
    printers = [p[2] for p in win32print.EnumPrinters(2)]

    classified = []
    for printer in printers:
        classified.append({
            "name": printer,
            "type": "thermal" if is_zebra_printer(printer) else "laser"
        })

    return jsonify(classified)

@bp.route("/printer", methods=["PUT"])
@require_session_token
def select_printer_route():

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Invalid JSON payload")

    role = data.get("role", "thermal")
    printer = data.get("printer")

    if role not in ("laser", "thermal"):
        abort(400, "Invalid role")

    if printer is not None and not isinstance(printer, str):
        abort(400, "Invalid printer name")

    set_printer(role, printer)

    log_event(
        f"SELECTED PRINTER | role={role} | printer={printer or 'NONE'}"
    )

    return jsonify({
        "status": "ok",
        "role": role,
        "printer": printer,
    })
