from core.agent_config import CONFIG, save_config

CURRENT_PRINTER = CONFIG.get("printer_name")

def set_printer(printer: str):
    global CURRENT_PRINTER
    CURRENT_PRINTER = printer
    CONFIG["printer_name"] = printer
    save_config()

def get_printer() -> str:
    return CURRENT_PRINTER
