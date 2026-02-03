import json
import os
from functools import lru_cache
from typing import Optional, Iterable


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

ZEBRA_CONFIG_PATH = os.path.join(
    BASE_DIR, "config", "zebra_printers.json"
)


@lru_cache(maxsize=1)
def load_zebra_prefixes() -> tuple[str, ...]:

    if not os.path.exists(ZEBRA_CONFIG_PATH):
        raise RuntimeError("zebra_printers.json not found")

    with open(ZEBRA_CONFIG_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise RuntimeError("Invalid zebra_printers.json format")

    known = data.get("known_models", [])
    custom = data.get("custom_names", [])

    if not isinstance(known, list) or not isinstance(custom, list):
        raise RuntimeError(
            "zebra_printers.json: known_models and custom_names must be lists"
        )

    prefixes: Iterable[str] = known + custom

    return tuple(
        prefix.strip().lower()
        for prefix in prefixes
        if isinstance(prefix, str) and prefix.strip()
    )


def is_zebra_printer(printer_name: Optional[str]) -> bool:
    if not printer_name:
        return False

    name = printer_name.strip().lower()

    prefixes = load_zebra_prefixes()

    return any(name.startswith(prefix) for prefix in prefixes)
