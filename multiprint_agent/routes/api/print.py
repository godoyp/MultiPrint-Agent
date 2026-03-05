from flask_smorest import Blueprint
from multiprint_agent.core.response import success_response
from multiprint_agent.modules.security.auth import require_session_token
from multiprint_agent.modules.security.rate_limit import rate_limited, PRINT_LIMIT, PRINT_WINDOW
from multiprint_agent.modules.schemas.print_schema import PrintRequestSchema, PrintResponseSchema
from multiprint_agent.modules.schemas.error_schema import ErrorResponseSchema
from multiprint_agent.modules.schemas.requests.print_request import PrintRequestDTO
from multiprint_agent.modules.schemas.responses.print_response import PrintResponseDTO
from multiprint_agent.modules.printing.services import process_print_request


bp = Blueprint("print", __name__, description="Printing operations")

@bp.route("/print", methods=["POST"])
@rate_limited(PRINT_LIMIT, PRINT_WINDOW)
@require_session_token
@bp.arguments(PrintRequestSchema)
@bp.response(200, PrintResponseSchema)
@bp.doc(
    responses={
        400: {"description": "Bad request", "schema": ErrorResponseSchema},
        401: {"description": "Unauthorized", "schema": ErrorResponseSchema},
        422: {"description": "Unprocessable entity", "schema": ErrorResponseSchema},
        429: {"description": "Rate limit exceeded", "schema": ErrorResponseSchema},
        500: {"description": "Internal server error", "schema": ErrorResponseSchema},
    }
)
def print_route(request_data):

    dto = PrintRequestDTO(request_data)

    try:
        result_data = process_print_request(dto)
        response = PrintResponseDTO(success=True, data=result_data)
    except Exception as e:
        response = PrintResponseDTO(success=False, error={"code": "internal_error", "message": str(e), "status": 500})
    
    return success_response(response.to_dict())