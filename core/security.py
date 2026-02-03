import os

class SecurityConfigError(RuntimeError):
    pass


def get_api_key() -> str:

    api_key = os.environ.get("MULTIPRINT_API_KEY")

    if not api_key:
        raise SecurityConfigError(
            "MULTIPRINT_API_KEY environment variable not set"
        )

    return api_key
