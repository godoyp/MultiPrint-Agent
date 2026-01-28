from modules.printer_utils import is_zebra
from modules.print_zebra import print_zebra
from modules.print_laser import print_laser
from modules.renderer import render_pdf
from modules.print_laser import print_laser_image

def dispatch_print(printer, payload):

    kind = payload["kind"]

    if kind == "pdf":
        images = render_pdf(payload["bytes"])
        print_laser_image(printer, images)
        return

    if is_zebra(printer):
        print_zebra(printer, payload["text"])
    else:
        print_laser(printer, payload["text"])
