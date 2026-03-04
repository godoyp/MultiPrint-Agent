from .limits import MAX_ZPL_BYTES, MAX_TEXT_BYTES, MAX_PDF_BYTES, MAX_IMAGE_BYTES
from .errors import PayloadValidationError
from .utils import payload_size_bytes


def validate_payload(payload: dict):
    kind = payload.get("kind")
    size = payload_size_bytes(payload)

    if size <= 0:
        raise PayloadValidationError("Empty or invalid payload")

    if kind == "zpl" and size > MAX_ZPL_BYTES:
        raise PayloadValidationError(
            f"ZPL payload too large ({size} bytes)"
        )

    if kind == "text" and size > MAX_TEXT_BYTES:
        raise PayloadValidationError(
            f"Text payload too large ({size} bytes)"
        )

    if kind == "pdf" and size > MAX_PDF_BYTES:
        raise PayloadValidationError(
            f"PDF payload too large ({size} bytes)"
        )

    if kind == "image" and size > MAX_IMAGE_BYTES:
        raise PayloadValidationError(
            f"Image payload too large ({size} bytes)"
        )

    if kind not in ("zpl", "text", "pdf", "image"):
        raise PayloadValidationError("Unsupported payload type")
