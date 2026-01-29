import base64

def detect_payload(raw, content_type=None, encoding=None):
    if isinstance(raw, str) and "^XA" in raw and "^XZ" in raw:
        return {
            "kind": "zpl",
            "raw": raw,
            "encoding": None
        }

    if encoding in ("base64", "b64") and isinstance(raw, str):
        decoded = base64.b64decode(raw)

        if content_type == "application/pdf" or decoded.startswith(b"%PDF"):
            return {
                "kind": "pdf",
                "raw": raw,          
                "encoding": "base64"
            }

        if decoded.startswith(b"\x89PNG") or decoded.startswith(b"\xFF\xD8"):
            return {
                "kind": "image",
                "raw": raw,
                "encoding": "base64"
            }

    return {
        "kind": "text",
        "raw": raw,
        "encoding": None
    }
