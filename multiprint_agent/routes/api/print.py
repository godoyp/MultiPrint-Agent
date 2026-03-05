from flask import Blueprint, request
from multiprint_agent.core.response import success_response
from multiprint_agent.modules.security.auth import require_session_token
from multiprint_agent.modules.security.rate_limit import rate_limited, PRINT_LIMIT, PRINT_WINDOW
from multiprint_agent.modules.printing.services import process_print_request


bp = Blueprint("print", __name__)


@bp.route("/print", methods=["POST"])
@rate_limited(PRINT_LIMIT, PRINT_WINDOW)
@require_session_token
def print_route():

    data = request.get_json(silent=True) or {}

    request_kind = data.get("kind", "print")

    result = process_print_request(data, request_kind)

    return success_response(result)