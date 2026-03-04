from flask import Blueprint, request
from multiprint_agent.core.response import success_response
from multiprint_agent.modules.security.session_tokens import issue_session
from multiprint_agent.modules.security.rate_limit import rate_limited, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW
from multiprint_agent.modules.security.config import get_session_ttl
from multiprint_agent.modules.security.policies import localhost_only
from multiprint_agent.modules.observability.eventlog import log_event


bp = Blueprint("auth", __name__)

@bp.route("/auth/handshake", methods=["POST"])
@rate_limited(HANDSHAKE_LIMIT, HANDSHAKE_WINDOW)
@localhost_only()
def handshake_route():

    ttl = get_session_ttl()
    token = issue_session(ttl)

    log_event(f"HANDSHAKE OK | IP={request.remote_addr}")

    return success_response({
        "token": token,
        "expires_in": ttl,
    })