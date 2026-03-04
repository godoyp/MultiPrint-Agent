from flask import Blueprint, request, abort
from multiprint_web_agent.core.response import success_response
from multiprint_web_agent.modules.security.session_tokens import issue_session
from multiprint_web_agent.modules.security.rate_limit import rate_limit, rate_key_from_request, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW
from multiprint_web_agent.modules.security.config import get_session_ttl
from multiprint_web_agent.modules.observability.eventlog import log_event


bp = Blueprint("auth", __name__)

@bp.route("/auth/handshake", methods=["POST"])
def handshake_route():

    key = rate_key_from_request(
        route="handshake",
        token=None,
        ip=request.remote_addr,
    )

    if not rate_limit(key, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW):
        log_event("RATE LIMIT | /auth/handshake")
        abort(429, "Too many handshake attempts")

    if request.remote_addr not in ("127.0.0.1", "::1"):
        log_event(f"HANDSHAKE BLOCKED | IP={request.remote_addr}")
        abort(401, "Unauthorized")

    ttl = get_session_ttl()
    token = issue_session(ttl)

    log_event(f"HANDSHAKE OK | IP={request.remote_addr}")

    return success_response({
        "token": token,
        "expires_in": ttl,
    })
