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

def is_thermal_printer_name(printer_name: str) -> bool:
    if not printer_name:
        return False

    name = printer_name.lower().strip()

    prefixes = (
        ZEBRA_PRINTERS.get("known_models", []) +
        ZEBRA_PRINTERS.get("custom_names", [])
    )

    for prefix in prefixes:
        p = prefix.lower()
        if name.startswith(p) or name.startswith(f"zebra {p}"):
            return True

    return False

# SAVE CONFIG AND SELECTED PRINTER

def save_config():
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=2, ensure_ascii=False)

def set_printer(role: str, printer: str | None):
    CONFIG.setdefault("printers", {})

    if printer:
        CONFIG["printers"][role] = {"name": printer}
    else:
        CONFIG["printers"].pop(role, None)

    save_config()


# EXPORT CONFIG VALUES

def get_version() -> str:
    return CONFIG.get("agent_version", "N/A")

def get_port() -> int:
    return CONFIG.get("agent_port", 9108)

def get_thermal_printer():
    return CONFIG.get("printers", {}).get("thermal", {}).get("name")


def get_laser_printer():
    return CONFIG.get("printers", {}).get("laser", {}).get("name")
