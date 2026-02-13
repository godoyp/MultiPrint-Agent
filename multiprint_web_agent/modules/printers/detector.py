import json
from functools import lru_cache
from typing import Optional, Iterable
from pathlib import Path
from multiprint_web_agent.core.paths import ZEBRA_CONFIG_PATH
from multiprint_web_agent.core.json_utils import load_json


@lru_cache(maxsize=1)
def load_zebra_prefixes() -> tuple[str, ...]:

    if not ZEBRA_CONFIG_PATH.exists():
        raise RuntimeError("zebra_printers.json not found")

    data = load_json(ZEBRA_CONFIG_PATH)

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