import time
from collections import defaultdict


# LIMITS

PRINT_LIMIT = 20
PRINT_WINDOW = 10          # seconds

TEST_PRINT_LIMIT = 5
TEST_PRINT_WINDOW = 30

HANDSHAKE_LIMIT = 5
HANDSHAKE_WINDOW = 60


_REQUESTS: dict[str, list[float]] = defaultdict(list)


def rate_limit(key: str, limit: int, window_seconds: int) -> bool:
    now = time.time()
    window_start = now - window_seconds

    timestamps = _REQUESTS[key]

    # remove old requests
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
