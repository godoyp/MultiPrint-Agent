from core.config import CONFIG

CURRENT_PRINTER = CONFIG["printer_name"]

def set_printer(printer: str):
    global CURRENT_PRINTER
    CURRENT_PRINTER = printer
    CONFIG["printer_name"] = printer

def get_printer():
    return CURRENT_PRINTER