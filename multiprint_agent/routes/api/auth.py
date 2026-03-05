from flask import request
from flask_smorest import Blueprint
from multiprint_agent.core.response import success_response
from multiprint_agent.modules.security.session_tokens import issue_session
from multiprint_agent.modules.security.rate_limit import rate_limited, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW
from multiprint_agent.modules.security.config import get_session_ttl
from multiprint_agent.modules.security.policies import localhost_only
from multiprint_agent.modules.observability.eventlog import log_event
from multiprint_agent.modules.schemas.handshake_schema import HandshakeResponseSchema
from multiprint_agent.modules.schemas.error_schema import ErrorResponseSchema


bp = Blueprint("auth", __name__, description="Authentication related endpoints")

@bp.route("/auth/handshake", methods=["POST"])
@bp.response(200, HandshakeResponseSchema)
@bp.doc(
    description="Inicia o handshake para autenticação. Retorna um token temporário que deve ser usado nas chamadas subsequentes.",
    responses={
        401: {"description": "Unauthorized", "schema": ErrorResponseSchema},
        429: {"description": "Rate limit exceeded", "schema": ErrorResponseSchema},
        500: {"description": "Internal server error", "schema": ErrorResponseSchema},
    },
)
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