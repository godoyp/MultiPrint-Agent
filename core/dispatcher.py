from modules.printer_utils import is_zebra
from modules.print_zebra import print_zebra
from modules.print_laser import print_laser

def dispatch_print(printer_name: str, payload: str):
    if is_zebra(printer_name):
        print_zebra(printer_name, payload)
    else:
        print_laser(printer_name, payload)
