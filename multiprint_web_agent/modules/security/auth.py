from functools import wraps
from flask import request, abort, g
from multiprint_web_agent.core.security import get_api_key, SecurityConfigError
from multiprint_web_agent.modules.security.session_tokens import validate_session


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        api_key = request.headers.get("X-API-KEY")

        try:
            expected_key = get_api_key()
        except SecurityConfigError:
            abort(500, "Server security misconfiguration")

        if not api_key or api_key != expected_key:
            abort(401, "Unauthorized")

        return func(*args, **kwargs)

    return wrapper


def require_session_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = (
            request.headers.get("Authorization", "")
            .replace("Bearer ", "")
            .strip()
            or request.headers.get("X-SESSION-TOKEN")
            or request.args.get("token")
        )

        if not token or not validate_session(token):
            abort(401, "Unauthorized")

        g.session_token = token

        return func(*args, **kwargs)

    return wrapper