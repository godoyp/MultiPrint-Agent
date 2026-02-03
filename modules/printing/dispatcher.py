from modules.printing.zebra import print_zebra
from modules.printing.laser import print_laser
from modules.printing.renderer import render_to_images


def dispatch_print(printer: str, payload: dict):
    kind = payload.get("kind")

    if not kind:
        raise ValueError("Payload kind not specified")

    if kind == "zpl":
        print_zebra(printer, payload["raw"])
        return

    images = render_to_images(payload)
    print_laser(printer, images)
