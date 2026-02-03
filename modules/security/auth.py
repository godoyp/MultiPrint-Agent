from flask import request, jsonify
from core.agent_config import get_api_key
from modules.security.session_tokens import validate_session


def require_api_key():
    
    api_key = request.headers.get("X-API-KEY")
    if api_key != get_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    return None


def require_session_token():
    token = (
        request.headers.get("Authorization", "")
        .replace("Bearer ", "")
        .strip()
        or request.headers.get("X-SESSION-TOKEN")
        or request.args.get("token")  # SSE
    )

    if not token or not validate_session(token):
        return jsonify({"error": "Unauthorized"}), 401

    return None
