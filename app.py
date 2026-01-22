import json
import win32print
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from modules.eventlog import log_event, event_stream
from modules.print_zebra import print_zebra
from modules.print_laser import print_laser
from modules.printer_utils import is_zebra

# CONFIG

with open("config.json", encoding="utf-8") as f:
    CONFIG = json.load(f)

PORT = CONFIG.get("port", 5000)
CURRENT_PRINTER = CONFIG["printer_name"]

# APP

app = Flask(__name__)
CORS(app)

# PRINT DISPATCHER

def dispatch_print(printer_name: str, payload: str):
    if is_zebra(printer_name):
        print_zebra(printer_name, payload)
    else:
        print_laser(printer_name, payload)

# PRINT ROUTE

@app.route("/print", methods=["POST"])
def print_label():
    data = request.get_json(force=True)

    raw = data.get("raw")
    if not raw:
        log_event("ERRO: Payload vazio")
        return jsonify({"error": "Payload vazio"}), 400

    try:
        dispatch_print(CURRENT_PRINTER, raw)

        log_event(
            f"OK | Printer={CURRENT_PRINTER} | "
            f"Bytes={len(raw)} | IP={request.remote_addr}"
        )

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"ERRO | {str(e)}")
        return jsonify({"error": str(e)}), 500

# LIST PRINTERS ROUTE

@app.route("/printers", methods=["GET"])
def list_printers():
    printers = [p[2] for p in win32print.EnumPrinters(2)]
    log_event("IMPRESSORAS ATUALIZADAS")
    return jsonify(printers)

# PRINTER HEALTH ROUTE

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "printer": CURRENT_PRINTER,
        "port": PORT
    })

# UI ROUTE

@app.route("/ui")
def ui():
    return send_from_directory("static", "ui.html")

# LOAD CURRENT PRINTER ROUTE

@app.route("/config", methods=["GET"])
def config():
    if request.method == "GET":
        return jsonify(CONFIG)

# SAVE SELECTED PRINTER ROUTE

@app.route("/config/printer", methods=["POST"])
def set_printer():
    global CURRENT_PRINTER

    data = request.get_json()
    printer = data.get("printer")

    if not printer:
        return jsonify({"error": "Impressora inválida"}), 400

    CURRENT_PRINTER = printer

    CONFIG["printer_name"] = printer
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=2, ensure_ascii=False)

    print(f"🖨️ Impressora alterada para: {printer}")
    log_event(f"IMPRESSORA SELECIONADA | {printer}")

    return jsonify({"status": "ok", "printer": printer})

# TEST PRINT ROUTE

@app.route("/test-print", methods=["POST"])
def test_print():
    try:
        if is_zebra(CURRENT_PRINTER):
            payload = (
                "^XA\r\n"
                "^PW800\r\n"
                "^LL480\r\n"
                "^FO40,30^A0N,50,50^FDTESTE DE IMPRESSAO^FS\r\n"
                "^FO40,90^A0N,30,30^FDLocalPrint Agent^FS\r\n"
                "^FO500,40^BQN,2,10^FDLA,LOCALPRINT-TEST-OK^FS\r\n"
                "^XZ\r\n"
            )
        else:
            payload = (
                "TESTE DE IMPRESSAO\n"
                "LocalPrint Agent\n"
                "Impressora configurada com sucesso.\n"
            )

        dispatch_print(CURRENT_PRINTER, payload)
        log_event("TESTE DE IMPRESSÃO | OK")

        return jsonify({"status": "ok"})

    except Exception as e:
        log_event(f"ERRO TESTE | {str(e)}")
        return jsonify({"error": str(e)}), 500
    
#  LOG ROUTE

@app.route("/logs/stream")
def logs_stream():
    return Response(event_stream(), mimetype="text/event-stream")

# VERSION ROUTE
@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": CONFIG.get("version", "N/A")})

# START

if __name__ == "__main__":
    print("🖨️ Agente de impressão iniciado")
    print(f"➡️ Impressora: {CURRENT_PRINTER}")
    print(f"🌐 https://localhost:{PORT}")
    app.run(host="127.0.0.1", port=PORT, ssl_context=("certs/localhost.crt", "certs/localhost.key"))
