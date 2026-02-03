from flask import Blueprint, request, jsonify
from modules.security.session_tokens import issue_session

bp = Blueprint("auth", __name__)

@bp.route("/auth/handshake", methods=["POST"])
def handshake_route():
    # Trust localhost UI
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Unauthorized"}), 401

    token = issue_session()

    return jsonify({
        "token": token,
        "expires_in": 1800
    })
