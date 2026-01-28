import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
ZEBRA_PATH = os.path.join(CONFIG_DIR, "zebra_printers.json")

# LOAD CONFIG

with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = json.load(f)

# LOAD ZEBRA LIB

with open(ZEBRA_PATH, encoding="utf-8") as f:
    ZEBRA_PRINTERS = json.load(f)

# SAVE CONFIG AND SELECTED PRINTER

def save_config():
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=2, ensure_ascii=False)

def set_printer(printer: str):
    CONFIG["printer_name"] = printer
    save_config()

# EXPORT CONFIG VALUES

def get_version() -> str:
    return CONFIG.get("agent_version", "N/A")

def get_port() -> str:
    return CONFIG.get("agent_port", 9108),

def get_printer() -> str:
    return CONFIG.get("printer_name")