import base64


def looks_like_base64(data: str) -> bool:
    try:
        base64.b64decode(data, validate=True)
        return True
    except Exception:
        return False


def detect_payload(raw, content_type=None, encoding=None):
 
    if encoding in ("base64", "b64"):
        data_bytes = base64.b64decode(raw)

        if content_type == "application/pdf" or data_bytes.startswith(b"%PDF"):
            return {
                "kind": "pdf",
                "text": None,
                "bytes": data_bytes
            }

    # ZPL explícito
    if isinstance(raw, str) and "^XA" in raw and "^XZ" in raw:
        return {
            "kind": "zpl",
            "text": raw,
            "bytes": None
        }

    # auto-detect base64 → PDF
    if isinstance(raw, str) and looks_like_base64(raw):
        data_bytes = base64.b64decode(raw)
        if data_bytes.startswith(b"%PDF"):
            return {
                "kind": "pdf",
                "text": None,
                "bytes": data_bytes
            }

    # fallback texto
    return {
        "kind": "text",
        "text": raw,
        "bytes": None
    }
