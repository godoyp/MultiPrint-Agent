from pathlib import Path
import sys


def get_package_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "multiprint_web_agent"

    return Path(__file__).resolve().parents[1]

PACKAGE_ROOT = get_package_root()

CONFIG_DIR = PACKAGE_ROOT / "config"
STATIC_DIR = PACKAGE_ROOT / "static"
CERTS_DIR = PACKAGE_ROOT / "certs"
LOGS_DIR = PACKAGE_ROOT / "logs"  

AGENT_CONFIG_PATH = CONFIG_DIR / "agent.json"
SECURITY_CONFIG_PATH = CONFIG_DIR / "security.json"
ZEBRA_CONFIG_PATH = CONFIG_DIR / "zebra_printers.json"

SSL_CERT_PATH = CERTS_DIR / "agent.crt"
SSL_KEY_PATH = CERTS_DIR / "agent.key"

LOGS_DIR = PACKAGE_ROOT / "logs"
AGENT_LOG_PATH = LOGS_DIR / "agent.log"