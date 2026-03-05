from multiprint_agent.modules.printing.dispatcher import dispatch_print
from multiprint_agent.modules.observability.eventlog import log_event
from multiprint_agent.modules.printers.utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from multiprint_agent.modules.payload.utils import detect_payload, payload_size_bytes
from multiprint_agent.modules.payload.validator import validate_payload
from multiprint_agent.modules.payload.errors import PayloadValidationError
from multiprint_agent.modules.test_assets import generate_laser_test_pdf_base64, generate_thermal_test_zpl
from multiprint_agent.core.agent_config import get_thermal_printer, get_laser_printer
from multiprint_agent.core.exceptions import BadRequestError, ConflictError, ServiceUnavailableError


def execute_print(printer, payload, request_mode):

    if not printer_is_online(printer):
        log_event(f"PRINT FAILED | request={request_mode} | PRINTER OFFLINE | {printer}")
        raise ServiceUnavailableError("Printer offline or unavailable")

    try:
        validate_payload(payload)
    except PayloadValidationError as e:
        log_event(f"PRINT REJECTED | request={request_mode} | {e.message}")
        raise BadRequestError(e.message)

    dispatch_print(printer, payload)

    size = payload_size_bytes(payload)
    log_event(f"PRINT OK | request={request_mode} | printer={printer} | payload={payload['kind']} | bytes={size}")

    return "ok"


def process_print_request(dto):

    request_mode = dto.mode

    if request_mode == "test":
        return build_test_print(request_mode)

    status = build_real_print(request_mode, dto.raw, dto.content_type, dto.encoding)
    return {"status": status}


def build_test_print(request_mode):

    thermal = get_thermal_printer()
    laser = get_laser_printer()

    if not thermal and not laser:
        raise BadRequestError("No printers configured")

    results = {"thermal": None, "laser": None}

    if thermal:
        payload = {
            "kind": "zpl",
            "raw": generate_thermal_test_zpl(thermal),
            "encoding": None,
        }
        results["thermal"] = execute_print(thermal, payload, request_mode)

    if laser:
        payload = detect_payload(
            raw=generate_laser_test_pdf_base64(laser),
            content_type="application/pdf",
        )
        results["laser"] = execute_print(laser, payload, request_mode)

    return results


def build_real_print(request_mode, raw, content_type, encoding):

    if not raw:
        raise BadRequestError("raw is required for real print")

    try:
        payload = detect_payload(raw=raw, content_type=content_type, encoding=encoding)
        printer = resolve_printer_by_payload(payload)
        return execute_print(printer, payload, request_mode)

    except PayloadValidationError as e:
        log_event(f"PRINT REJECTED | request={request_mode} | {e.message}")
        raise BadRequestError(e.message)

    except PrinterNotConfiguredError as e:
        log_event(f"PRINT FAILED | request={request_mode} | {str(e)}")
        raise ConflictError(str(e))
    