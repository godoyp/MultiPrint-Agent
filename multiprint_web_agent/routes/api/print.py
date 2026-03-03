from flask import Blueprint, request, jsonify
from multiprint_web_agent.modules.printing.dispatcher import dispatch_print
from multiprint_web_agent.modules.observability.eventlog import log_event
from multiprint_web_agent.modules.printers.utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from multiprint_web_agent.modules.payload.utils import detect_payload, payload_size_bytes
from multiprint_web_agent.modules.payload.validator import validate_payload
from multiprint_web_agent.modules.payload.errors import PayloadValidationError
from multiprint_web_agent.modules.security.auth import require_session_token
from multiprint_web_agent.modules.security.rate_limit import rate_limit, rate_key_from_request, PRINT_LIMIT, PRINT_WINDOW


bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def print_route():

    auth = require_session_token()
    if auth:
        return auth

    token = (
        request.headers.get("Authorization", "")
        .replace("Bearer ", "")
        .strip()
    )

    key = rate_key_from_request(
        route="print",
        token=token,
        ip=request.remote_addr,
    )

    if not rate_limit(key, PRINT_LIMIT, PRINT_WINDOW):
        log_event("RATE LIMIT | /print")
        return jsonify({"error": "Rate limit exceeded"}), 429


    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    raw = data.get("raw")
    if not raw:
        return jsonify({"error": "raw is required"}), 400
    
    try:
        payload = detect_payload(
            raw=raw,
            content_type=data.get("contentType"),
            encoding=data.get("encoding"),
        )

        validate_payload(payload)

    except PayloadValidationError as e:
        log_event(f"PRINT REJECTED | {e.message}")
        return jsonify({"error": e.message}), 400
    
    try:
        printer = resolve_printer_by_payload(payload)

        if not printer_is_online(printer):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {printer}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": printer,
            }), 503

        dispatch_print(printer, payload)

    except PrinterNotConfiguredError as e:
        log_event(f"PRINT FAILED | {str(e)}")
        return jsonify({"error": str(e)}), 409
    
    except Exception as e:
        log_event(f"PRINT ERROR | {str(e)}")
        return jsonify({"error": "Internal print error"}), 500

    size = payload_size_bytes(payload)

    log_event(
        f"PRINT OK | printer={printer} | type={payload['kind']} | bytes={size}"
    )

    return jsonify({"status": "ok"})
