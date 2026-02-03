import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

AGENT_PATH = os.path.join(CONFIG_DIR, "agent.json")


# LOAD AGENT CONFIG (once, in memory)

with open(AGENT_PATH, encoding="utf-8") as f:
    AGENT_CONFIG = json.load(f)


# AGENT CONFIG (state)

def save_agent_config():
    with open(AGENT_PATH, "w", encoding="utf-8") as f:
        json.dump(AGENT_CONFIG, f, indent=2, ensure_ascii=False)


def set_printer(role: str, printer: str | None):
    AGENT_CONFIG.setdefault("printers", {})
    AGENT_CONFIG["printers"].setdefault("thermal", {"name": None})
    AGENT_CONFIG["printers"].setdefault("laser", {"name": None})

    if role not in ("thermal", "laser"):
        raise ValueError(f"Invalid printer role: {role}")

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
