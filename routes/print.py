from flask import Blueprint, request, jsonify
from core.dispatcher import dispatch_print
from modules.eventlog import log_event
from modules.printer_utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from modules.payload_utils import detect_payload


bp = Blueprint("print", __name__)

@bp.route("/print", methods=["POST"])
def print_route():
    data = request.get_json(force=True, silent=True)

    if not data or "raw" not in data:
        return jsonify({"error": "raw is required"}), 400

    try:
        payload = detect_payload(
            raw=data["raw"],
            content_type=data.get("contentType"),
            encoding=data.get("encoding"),
        )

        printer = resolve_printer_by_payload(payload)

        if not printer_is_online(printer):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {printer}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": printer
            }), 503

        dispatch_print(printer, payload)

        log_event(
            f"PRINT OK | printer={printer} | type={payload['kind']}"
        )

        return jsonify({"status": "ok"})

    except PrinterNotConfiguredError as e:
        log_event(f"PRINT FAILED | {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        log_event(f"PRINT ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
