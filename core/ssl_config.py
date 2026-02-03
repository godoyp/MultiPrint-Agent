import os

CERT_PATH = "certs/agent.crt"
KEY_PATH = "certs/agent.key"


def get_ssl_context():
    enable_https = os.environ.get(
        "MULTIPRINT_ENABLE_HTTPS", "true"
    ).lower()

    if enable_https not in ("1", "true", "yes"):
        return None

    if not os.path.exists(CERT_PATH) or not os.path.exists(KEY_PATH):
        raise RuntimeError(
            "HTTPS enabled but SSL certificate files not found"
        )

    return (CERT_PATH, KEY_PATH)
