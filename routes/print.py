from flask import Blueprint, request, jsonify
from core.dispatcher import dispatch_print
from core.printer_state import CURRENT_PRINTER
from modules.eventlog import log_event

bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def send_print():
    data = request.get_json(force=True)
    raw = data.get("raw")

    if not raw:
        log_event("ERROR: Empty Payload")
        return jsonify({"error": "Empty Payload"}), 400

    try:
        dispatch_print(CURRENT_PRINTER, raw)

        log_event(
            f"OK | Printer={CURRENT_PRINTER} | "
            f"Bytes={len(raw)} | IP={request.remote_addr}"
        )

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
