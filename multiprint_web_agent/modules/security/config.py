from multiprint_web_agent.core.paths import SECURITY_CONFIG_PATH
from multiprint_web_agent.core.json_utils import load_json
from multiprint_web_agent.core.constants import DEFAULT_SESSION_TTL


def get_session_ttl() -> int:
    data = load_json(SECURITY_CONFIG_PATH, default={})
    
    return int(data.get("session_ttl", DEFAULT_SESSION_TTL))