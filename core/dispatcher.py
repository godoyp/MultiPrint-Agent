from modules.print_zebra import print_zebra
from modules.print_laser import print_laser
from modules.renderer import render_to_images


def dispatch_print(printer: str, payload: dict):
    kind = payload.get("kind")

    if not kind:
        raise ValueError("Payload kind not specified")

    if kind == "zpl":
        print_zebra(printer, payload["raw"])
        return

    images = render_to_images(payload)
    print_laser(printer, images)
