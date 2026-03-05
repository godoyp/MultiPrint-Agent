from flask import jsonify
from multiprint_agent.core.response import error_response
from multiprint_agent.core.exceptions import AppError
from multiprint_agent.modules.schemas.error_schema import ErrorResponseSchema


def register_api_error_handlers(api_blueprint):

    @api_blueprint.errorhandler(AppError)
    @api_blueprint.doc(responses={AppError.status_code: ErrorResponseSchema})
    def handle_app_error(e):
        return error_response(
            code=e.error_code,
            message=e.message,
            status_code=e.status_code
        )

    @api_blueprint.errorhandler(Exception)
    @api_blueprint.doc(responses={500: ErrorResponseSchema})
    def handle_unexpected_exception(e):
        return error_response(
            code="internal_error",
            message="Unexpected server error",
            status_code=500
        )


def register_ui_error_handlers(ui_blueprint):

    @ui_blueprint.errorhandler(AppError)
    def handle_ui_app_error(e):
        return jsonify({
            "error": e.message,
            "status": e.status_code
        }), e.status_code

    @ui_blueprint.errorhandler(Exception)
    def handle_ui_unexpected_exception(e):
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500
    