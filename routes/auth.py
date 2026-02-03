from flask import Blueprint, request, jsonify
from modules.security.session_tokens import issue_session
from modules.security.rate_limit import rate_limit, rate_key_from_request, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW

bp = Blueprint("auth", __name__)

@bp.route("/auth/handshake", methods=["POST"])
def handshake_route():

    # Rate Limit (IP Based)

    key = rate_key_from_request(
        route="handshake",
        token=None,
        ip=request.remote_addr
    )

    if not rate_limit(key, HANDSHAKE_LIMIT, HANDSHAKE_WINDOW):
        return jsonify({
            "error": "Too many handshake attempts"
        }), 429
    
    # Trust localhost UI
    
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Unauthorized"}), 401

    token = issue_session()

    return jsonify({
        "token": token,
        "expires_in": 1800
    })
