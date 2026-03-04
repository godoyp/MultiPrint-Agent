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

def payload_size_bytes(payload: dict) -> int:
    raw = payload.get("raw")
    encoding = payload.get("encoding")

    if raw is None:
        return 0

    # base64 payloads (PDF, image, etc)
    if encoding in ("base64", "b64") and isinstance(raw, str):
        try:
            return len(base64.b64decode(raw))
        except Exception:
            return 0

    # plain string (ZPL / text)
    if isinstance(raw, str):
        return len(raw.encode("utf-8"))

    # raw bytes (future-proof)
    if isinstance(raw, (bytes, bytearray)):
        return len(raw)

    return 0
