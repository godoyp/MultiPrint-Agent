from flask import jsonify


def success_response(data=None, status_code=200):
    return jsonify({
        "success": True,
        "data": data,
        "error": None
    }), status_code


def error_response(code, message, status_code=400):
    return jsonify({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }), status_code