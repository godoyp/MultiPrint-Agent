from .paths import AGENT_CONFIG_PATH
from multiprint_agent.core.json_utils import load_json, save_json
from multiprint_agent.core.constants import DEFAULT_AGENT_PORT


AGENT_CONFIG = load_json(AGENT_CONFIG_PATH)

def save_agent_config():
    save_json(AGENT_CONFIG_PATH, AGENT_CONFIG)


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
    return AGENT_CONFIG.get("agent_port", DEFAULT_AGENT_PORT)


def get_thermal_printer() -> str | None:
    return AGENT_CONFIG.get("printers", {}).get("thermal", {}).get("name")


def get_laser_printer() -> str | None:
    return AGENT_CONFIG.get("printers", {}).get("laser", {}).get("name")
