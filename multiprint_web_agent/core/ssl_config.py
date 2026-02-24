import os
from .paths import SSL_CERT_PATH, SSL_KEY_PATH


def get_ssl_context():
    enable_https = os.environ.get(
        "MULTIPRINT_ENABLE_HTTPS", "true"
    ).lower()

    if enable_https not in ("1", "true", "yes"):
        return None

    if not SSL_CERT_PATH.exists() or not SSL_KEY_PATH.exists():
        raise RuntimeError(
            "HTTPS enabled but SSL certificate files not found"
        )

    return (str(SSL_CERT_PATH), str(SSL_KEY_PATH))