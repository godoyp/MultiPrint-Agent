import win32print
from flask import Blueprint, jsonify
from modules.eventlog import log_event

bp = Blueprint("printers", __name__)

@bp.route("/printers", methods=["GET"])
def list_printers():
    printers = [p[2] for p in win32print.EnumPrinters(2)]
    log_event("PRINTER LIST UPDATED")
    return jsonify(printers)
