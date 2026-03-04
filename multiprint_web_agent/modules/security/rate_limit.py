import time
from collections import defaultdict
from functools import wraps
from flask import request, g
from multiprint_web_agent.modules.observability.eventlog import log_event
from multiprint_web_agent.core.exceptions import TooManyRequestsError


PRINT_LIMIT = 20
PRINT_WINDOW = 10

TEST_PRINT_LIMIT = 5
TEST_PRINT_WINDOW = 30

HANDSHAKE_LIMIT = 5
HANDSHAKE_WINDOW = 60


_REQUESTS: dict[str, list[float]] = defaultdict(list)


def rate_limit_check(key: str, limit: int, window_seconds: int) -> bool:
    now = time.time()
    window_start = now - window_seconds

    timestamps = _REQUESTS[key]

    while timestamps and timestamps[0] < window_start:
        timestamps.pop(0)

    if len(timestamps) >= limit:
        return False

    timestamps.append(now)
    return True


def rate_key_from_request(route: str, token: str | None, ip: str) -> str:
    if token:
        return f"{route}:token:{token}"
    return f"{route}:ip:{ip}"


def rate_limited(limit: int, window: int):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            token = getattr(g, "session_token", None)
            ip = request.remote_addr
            route = request.endpoint or "unknown"

            key = rate_key_from_request(route, token, ip)

            if not rate_limit_check(key, limit, window):
                log_event("RATE LIMIT EXCEEDED")
                raise TooManyRequestsError("Rate limit exceeded")

            return f(*args, **kwargs)

        return wrapper
    return decorator