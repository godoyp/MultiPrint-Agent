from multiprint_agent.modules.printing.dispatcher import dispatch_print
from multiprint_agent.modules.observability.eventlog import log_event
from multiprint_agent.modules.printers.utils import printer_is_online, resolve_printer_by_payload, PrinterNotConfiguredError
from multiprint_agent.modules.payload.utils import detect_payload, payload_size_bytes
from multiprint_agent.modules.payload.validator import validate_payload
from multiprint_agent.modules.payload.errors import PayloadValidationError
from multiprint_agent.modules.test_assets import generate_laser_test_pdf_base64, generate_thermal_test_zpl
from multiprint_agent.core.agent_config import get_thermal_printer, get_laser_printer
from multiprint_agent.core.exceptions import BadRequestError, ConflictError, ServiceUnavailableError


def process_print_request(data: dict, request_kind: str):

    if request_kind == "test":

        thermal = get_thermal_printer()
        laser = get_laser_printer()

        if not thermal and not laser:
            raise BadRequestError("No printers configured")

        results = {"thermal": None, "laser": None}

        if thermal:
            if not printer_is_online(thermal):
                log_event(f"PRINT FAILED | request={request_kind} | PRINTER OFFLINE | {thermal}")
                results["thermal"] = "offline"
            else:

                raw = generate_thermal_test_zpl(thermal)

                payload = {
                    "kind": "zpl",
                    "raw": raw,
                    "encoding": None,
                }

                validate_payload(payload)

                dispatch_print(thermal, payload)

                size = payload_size_bytes(payload)

                log_event(
                    f"PRINT OK | request={request_kind} | printer={thermal} | payload={payload['kind']} | bytes={size}"
                )

                results["thermal"] = "ok"

        if laser:
            if not printer_is_online(laser):
                log_event(f"PRINT FAILED | request={request_kind} | PRINTER OFFLINE | {laser}")
                results["laser"] = "offline"
            else:

                raw = generate_laser_test_pdf_base64(laser)

                payload = detect_payload(
                    raw=raw,
                    content_type="application/pdf",
                    encoding="base64",
                )

                validate_payload(payload)

                dispatch_print(laser, payload)

                size = payload_size_bytes(payload)

                log_event(
                    f"PRINT OK | request={request_kind} | printer={laser} | payload={payload['kind']} | bytes={size}"
                )

                results["laser"] = "ok"

        return results

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

        log_event(f"PRINT REJECTED | request={request_kind} | {e.message}")
        raise BadRequestError(e.message)

    try:

        printer = resolve_printer_by_payload(payload)

        if not printer_is_online(printer):

            log_event(
                f"PRINT FAILED | request={request_kind} | PRINTER OFFLINE | {printer}"
            )

            raise ServiceUnavailableError("Printer offline or unavailable")

        dispatch_print(printer, payload)

    except PrinterNotConfiguredError as e:

        log_event(f"PRINT FAILED | request={request_kind} | {str(e)}")
        raise ConflictError(str(e))

    size = payload_size_bytes(payload)

    log_event(
        f"PRINT OK | request={request_kind} | printer={printer} | payload={payload['kind']} | bytes={size}"
    )

    return {"status": "ok"}