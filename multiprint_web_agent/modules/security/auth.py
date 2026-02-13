from flask import request, jsonify
from multiprint_web_agent.core.security import get_api_key, SecurityConfigError
from .session_tokens import validate_session


def require_api_key():
    api_key = request.headers.get("X-API-KEY")

    try:
        expected_key = get_api_key()
    except SecurityConfigError as e:
        return jsonify({"error": "Server security misconfiguration"}), 500

    if not api_key or api_key != expected_key:
        return jsonify({"error": "Unauthorized"}), 401

    return None


def require_session_token():
    token = (
        request.headers.get("Authorization", "")
        .replace("Bearer ", "")
        .strip()
        or request.headers.get("X-SESSION-TOKEN")
        or request.args.get("token") 
    )

    if not token or not validate_session(token):
        return jsonify({"error": "Unauthorized"}), 401

    return None
