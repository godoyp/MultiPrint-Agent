from flask import Blueprint, jsonify
from core.dispatcher import dispatch_print
from core.agent_config import get_printer
from modules.printer_utils import is_zebra, printer_is_online
from modules.eventlog import log_event

bp = Blueprint("print_test", __name__)

@bp.route("/test-print", methods=["POST"])
def test_print():
    printer = get_printer()

    try:
        if not printer_is_online(printer):
            log_event(f"PRINT TEST FAILED | PRINTER OFFLINE | {printer}")
            return jsonify({
                "error": "Printer offline or unavailable",
                "printer": printer
            }), 503
        
        if is_zebra(printer):
            payload = (
                "^XA\r\n"
                "^PW800\r\n"
                "^LL480\r\n"
                "^FO40,30^A0N,50,50^FDPRINT TEST^FS\r\n"
                "^FO40,90^A0N,30,30^FDMultiPrint Web Agent^FS\r\n"
                "^FO500,40^BQN,2,10^FDLA,PRINT-TEST-OK^FS\r\n"
                "^XZ\r\n"
            )
        else:
            payload = (
                "\n\n"
                "======================================\n"
                "               PRINT TEST             \n"
                "--------------------------------------\n"
                "            MultiPrint Web Agent      \n"
                "     Printer configured successfully \n"
                "======================================\n\n\n"
            )

        dispatch_print(printer, payload)
        log_event("PRINT TEST | OK")

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"TEST ERROR | {str(e)}")
        return jsonify({"error": str(e)}), 500
