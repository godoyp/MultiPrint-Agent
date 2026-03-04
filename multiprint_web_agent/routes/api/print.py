from flask import Blueprint, request
from multiprint_web_agent.core.response import success_response
from multiprint_web_agent.modules.printing.dispatcher import dispatch_print
from multiprint_web_agent.modules.observability.eventlog import log_event
from multiprint_web_agent.modules.printers.utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from multiprint_web_agent.modules.payload.utils import detect_payload, payload_size_bytes
from multiprint_web_agent.modules.payload.validator import validate_payload
from multiprint_web_agent.modules.payload.errors import PayloadValidationError
from multiprint_web_agent.modules.security.auth import require_session_token
from multiprint_web_agent.modules.security.rate_limit import rate_limited, PRINT_LIMIT, PRINT_WINDOW
from multiprint_web_agent.core.exceptions import BadRequestError, ConflictError, ServiceUnavailableError


bp = Blueprint("print", __name__)


@bp.route("/print", methods=["POST"])
@rate_limited(PRINT_LIMIT, PRINT_WINDOW)
@require_session_token
def print_route():

    data = request.get_json(silent=True)
    if not data:
        raise BadRequestError("Invalid JSON payload")

    raw = data.get("raw")
    if not raw:
        raise BadRequestError("raw is required")

    try:
        payload = detect_payload(
            raw=raw,
            content_type=data.get("contentType"),
            encoding=data.get("encoding"),
        )
        validate_payload(payload)

    except PayloadValidationError as e:
        log_event(f"PRINT REJECTED | {e.message}")
        raise BadRequestError(e.message)

    try:
        printer = resolve_printer_by_payload(payload)

        if not printer_is_online(printer):
            log_event(f"PRINT FAILED | PRINTER OFFLINE | {printer}")
            raise ServiceUnavailableError("Printer offline or unavailable")

        dispatch_print(printer, payload)

    except PrinterNotConfiguredError as e:
        log_event(f"PRINT FAILED | {str(e)}")
        raise ConflictError(str(e))

    size = payload_size_bytes(payload)

    log_event(
        f"PRINT OK | printer={printer} | type={payload['kind']} | bytes={size}"
    )

    return success_response({"status": "ok"})
