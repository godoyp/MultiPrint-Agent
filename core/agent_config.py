import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

AGENT_PATH = os.path.join(CONFIG_DIR, "agent.json")
SECURITY_PATH = os.path.join(CONFIG_DIR, "security.json")
ZEBRA_PATH = os.path.join(CONFIG_DIR, "zebra_printers.json")


# LOAD FILES (once, in memory)

with open(AGENT_PATH, encoding="utf-8") as f:
    AGENT_CONFIG = json.load(f)

with open(SECURITY_PATH, encoding="utf-8") as f:
    SECURITY_CONFIG = json.load(f)

with open(ZEBRA_PATH, encoding="utf-8") as f:
    ZEBRA_PRINTERS = json.load(f)


# PRINTER HELPERS

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


# AGENT CONFIG (state)

def save_agent_config():
    with open(AGENT_PATH, "w", encoding="utf-8") as f:
        json.dump(AGENT_CONFIG, f, indent=2, ensure_ascii=False)

def set_printer(role: str, printer: str | None):

    AGENT_CONFIG.setdefault("printers", {})
    AGENT_CONFIG["printers"].setdefault("thermal", {"name": None})
    AGENT_CONFIG["printers"].setdefault("laser", {"name": None})

    AGENT_CONFIG["printers"][role]["name"] = printer

    save_agent_config()


# READ-ONLY EXPORTS

def get_version() -> str:
    return AGENT_CONFIG.get("agent_version", "N/A")

def get_port() -> int:
    return AGENT_CONFIG.get("agent_port", 9108)

def get_thermal_printer() -> str | None:
    return AGENT_CONFIG.get("printers", {}).get("thermal", {}).get("name")

def get_laser_printer() -> str | None:
    return AGENT_CONFIG.get("printers", {}).get("laser", {}).get("name")


# SECURITY 

def get_api_key() -> str:
    return SECURITY_CONFIG.get("api_key")
