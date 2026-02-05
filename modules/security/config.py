import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SECURITY_PATH = os.path.join(CONFIG_DIR, "security.json")

DEFAULT_SESSION_TTL = 1800


def get_session_ttl() -> int:
    try:
        with open(SECURITY_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return DEFAULT_SESSION_TTL

    return int(data.get("session_ttl", DEFAULT_SESSION_TTL))