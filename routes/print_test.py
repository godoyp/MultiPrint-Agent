from flask import Blueprint, jsonify
from core.dispatcher import dispatch_print
from core.agent_config import get_thermal_printer, get_laser_printer
from modules.printer_utils import printer_is_online
from modules.eventlog import log_event
from modules.test_assets import generate_laser_test_pdf_base64
from modules.payload_utils import detect_payload, payload_size_bytes

bp = Blueprint("print_test", __name__)

@bp.route("/test-print", methods=["POST"])
def test_print():
    thermal = get_thermal_printer()
    laser = get_laser_printer()

    if not thermal and not laser:
        return jsonify({
            "error": "No printers configured"
        }), 400

    try:
        if thermal:
            if not printer_is_online(thermal):
                log_event(f"TEST PRINT | THERMAL OFFLINE | {thermal}")
            else:
                zpl_payload = (
                    "^XA\r\n"
                    "^PW800\r\n"
                    "^LL480\r\n"
                    "^FO40,30^A0N,50,50^FDPRINT TEST^FS\r\n"
                    "^FO40,90^A0N,30,30^FDMultiPrint Web Agent^FS\r\n"
                    "^FO500,40^BQN,2,10^FDLA,PRINT-TEST-OK^FS\r\n"
                    "^XZ\r\n"
                )

                payload = {
                    "kind": "zpl",
                    "raw": zpl_payload
                }

                size = payload_size_bytes(payload)

                dispatch_print(thermal, payload)
                log_event(f"TEST PRINT | THERMAL OK | {thermal} | BYTES= {size}")

        if laser:
            if not printer_is_online(laser):
                log_event(f"TEST PRINT | LASER OFFLINE | {laser}")
            else:
                raw = generate_laser_test_pdf_base64(laser)

                payload = detect_payload(
                    raw=raw,
                    content_type="application/pdf",
                    encoding="base64"
                )

                size = payload_size_bytes(payload)

                dispatch_print(laser, payload)
                log_event(f"TEST PRINT | LASER OK | {laser} | BYTES= {size}")

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"TEST PRINT ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
