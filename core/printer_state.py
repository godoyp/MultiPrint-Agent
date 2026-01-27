from core.agent_config import CONFIG, save_config

def set_printer(printer: str):
    CONFIG["printer_name"] = printer
    save_config()

def get_printer() -> str:
    return CONFIG.get("printer_name")
