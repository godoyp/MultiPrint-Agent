from flask import jsonify
from werkzeug.exceptions import HTTPException
from multiprint_web_agent.core.response import error_response


def register_api_error_handlers(api_blueprint):

    @api_blueprint.errorhandler(HTTPException)
    def handle_api_http_exception(e):
        return error_response(
            code=e.name.upper().replace(" ", "_"),
            message=e.description,
            status_code=e.code
        )

    @api_blueprint.errorhandler(Exception)
    def handle_api_unexpected_exception(e):
        return error_response(
            code="INTERNAL_SERVER_ERROR",
            message="Erro interno inesperado",
            status_code=500
        )


def register_ui_error_handlers(ui_blueprint):

    @ui_blueprint.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "error": e.description,
            "status": e.code
        }), e.code

    @ui_blueprint.errorhandler(Exception)
    def handle_unexpected_exception(e):
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500