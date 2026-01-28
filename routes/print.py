from flask import Blueprint, request, jsonify
from core.dispatcher import dispatch_print
from core.agent_config import get_printer
from modules.eventlog import log_event
from modules.printer_utils import printer_is_online
from modules.payload_utils import detect_payload


bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def send_print():
    data = request.get_json(force=True)
    raw = data.get("raw")
    content_type = data.get("contentType")
    encoding = data.get("encoding")

    if not raw:
        log_event("ERROR: Empty Payload")
        return jsonify({"error": "Empty Payload"}), 400

    printer = get_printer()

    try:
        if not printer_is_online(printer):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {printer}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": printer
            }), 503

        payload = detect_payload(raw, content_type, encoding)

        dispatch_print(printer, payload)

        log_event(
            f"OK | Printer={printer} | "
            f"Bytes={len(payload)} | IP={request.remote_addr}"
        )

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
