from flask import Blueprint, request, jsonify
from core.dispatcher import dispatch_print
from core.printer_state import CURRENT_PRINTER
from modules.eventlog import log_event
from modules.printer_utils import printer_is_online

bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def send_print():
    data = request.get_json(force=True)
    raw = data.get("raw")

    if not raw:
        log_event("ERROR: Empty Payload")
        return jsonify({"error": "Empty Payload"}), 400

    try:
        if not printer_is_online(CURRENT_PRINTER):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {CURRENT_PRINTER}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": CURRENT_PRINTER
            }), 503
        
        dispatch_print(CURRENT_PRINTER, raw)

        log_event(
            f"OK | Printer={CURRENT_PRINTER} | "
            f"Bytes={len(raw)} | IP={request.remote_addr}"
        )

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
