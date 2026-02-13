import secrets
import time

_SESSIONS: dict[str, float] = {}

def issue_session(ttl: int) -> str:
    token = secrets.token_urlsafe(32)
    _SESSIONS[token] = time.time() + ttl
    return token

def validate_session(token: str) -> bool:
    exp = _SESSIONS.get(token)
    if not exp:
        return False
    if time.time() > exp:
        _SESSIONS.pop(token, None)
        return False
    return True

def revoke_all_sessions():
    _SESSIONS.clear()
