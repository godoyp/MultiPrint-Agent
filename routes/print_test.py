from flask import Blueprint, jsonify
from core.dispatcher import dispatch_print
from core.printer_state import CURRENT_PRINTER
from modules.printer_utils import is_zebra
from modules.eventlog import log_event

bp = Blueprint("print_test", __name__)

@bp.route("/test-print", methods=["POST"])
def test_print():
    try:
        if is_zebra(CURRENT_PRINTER):
            payload = (
                "^XA\r\n"
                "^PW800\r\n"
                "^LL480\r\n"
                "^FO40,30^A0N,50,50^FDPRINT TEST^FS\r\n"
                "^FO40,90^A0N,30,30^FDLocalPrint Agent^FS\r\n"
                "^FO500,40^BQN,2,10^FDLA,LOCALPRINT-TEST-OK^FS\r\n"
                "^XZ\r\n"
            )
        else:
            payload = (
                "PRINT TEST\n"
                "LocalPrint Agent\n"
                "Printer configured successfully.\n"
            )

        dispatch_print(CURRENT_PRINTER, payload)
        log_event("PRINT TEST | OK")

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"TEST ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
