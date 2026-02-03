from flask import Blueprint, request, jsonify
from modules.printing.dispatcher import dispatch_print
from modules.observability.eventlog import log_event
from modules.printers.utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from modules.payload.utils import detect_payload, payload_size_bytes
from modules.payload.validator import validate_payload
from modules.payload.errors import PayloadValidationError
from modules.security.auth import require_session_token


bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def print_route():

    auth = require_session_token()
    if auth:
        return auth

    data = request.get_json(force=True, silent=True)

    if not data or "raw" not in data:
        return jsonify({"error": "raw is required"}), 400

    try:
   
        payload = detect_payload(
            raw=data["raw"],
            content_type=data.get("contentType"),
            encoding=data.get("encoding"),
        )

        validate_payload(payload)

        printer = resolve_printer_by_payload(payload)

        if not printer_is_online(printer):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {printer}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": printer
            }), 503

        dispatch_print(printer, payload)

        size = payload_size_bytes(payload)

        log_event(
            f"PRINT OK | printer={printer} | type={payload['kind']} | bytes={size}"
        )

        return jsonify({"status": "ok"})

    except PayloadValidationError as e:
        log_event(f"PRINT REJECTED | {e.message}")
        return jsonify({"error": e.message}), 400

    except PrinterNotConfiguredError as e:
        log_event(f"PRINT FAILED | {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        log_event(f"PRINT ERROR | {str(e)}")
        return jsonify({"error": "Internal print error"}), 500
