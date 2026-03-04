from functools import wraps
from flask import request, abort
from multiprint_web_agent.modules.observability.eventlog import log_event


def localhost_only():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            ip = request.remote_addr

            if ip not in ("127.0.0.1", "::1"):
                log_event(f"HANDSHAKE BLOCKED | IP={ip}")
                abort(401, "Unauthorized")

            return f(*args, **kwargs)

        return wrapper
    return decorator