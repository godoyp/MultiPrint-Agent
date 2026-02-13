from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]

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