from flask import Blueprint, jsonify
from modules.printing.dispatcher import dispatch_print
from core.agent_config import get_thermal_printer, get_laser_printer
from modules.printers.utils import printer_is_online
from modules.observability.eventlog import log_event
from modules.test_assets import generate_laser_test_pdf_base64, generate_thermal_test_zpl
from modules.payload.utils import detect_payload, payload_size_bytes
from modules.payload.validator import validate_payload
from modules.payload.errors import PayloadValidationError
from modules.security.auth import require_session_token


bp = Blueprint("print_test", __name__)

@bp.route("/test-print", methods=["POST"])
def print_test_route():

    auth = require_session_token()
    if auth:
        return auth

    thermal = get_thermal_printer()
    laser = get_laser_printer()

    if not thermal and not laser:
        return jsonify({
            "error": "No printers configured"
        }), 400

    results = {
        "thermal": None,
        "laser": None
    }

    try:

        if thermal:
            if not printer_is_online(thermal):
                log_event(f"TEST PRINT | THERMAL OFFLINE | {thermal}")
                results["thermal"] = "offline"
            else:

                raw = generate_thermal_test_zpl(thermal)

                payload = {
                    "kind": "zpl",
                    "raw": raw,
                    "encoding": None
                }

                validate_payload(payload)

                size = payload_size_bytes(payload)

                dispatch_print(thermal, payload)
                log_event(
                    f"TEST PRINT | THERMAL OK | {thermal} | BYTES={size}"
                )
                results["thermal"] = "ok"

        if laser:
            if not printer_is_online(laser):
                log_event(f"TEST PRINT | LASER OFFLINE | {laser}")
                results["laser"] = "offline"
            else:
                raw = generate_laser_test_pdf_base64(laser)

                payload = detect_payload(
                    raw=raw,
                    content_type="application/pdf",
                    encoding="base64"
                )

                validate_payload(payload)

                size = payload_size_bytes(payload)

                dispatch_print(laser, payload)
                log_event(
                    f"TEST PRINT | LASER OK | {laser} | BYTES={size}"
                )
                results["laser"] = "ok"

        if all(v == "offline" for v in results.values() if v is not None):
            return jsonify(results), 503

        if any(v == "offline" for v in results.values()):
            return jsonify(results), 207  

        return jsonify(results), 200

    except PayloadValidationError as e:
        log_event(f"TEST PRINT REJECTED | {e.message}")
        return jsonify({"error": e.message}), 400

    except Exception as e:
        log_event(f"TEST PRINT ERROR | {str(e)}")
        return jsonify({"error": "Internal test print error"}), 500
