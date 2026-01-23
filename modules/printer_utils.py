import win32print

import win32print
import win32ui
import pywintypes

def printer_is_online(printer_name: str) -> bool:
    try:
        handle = win32print.OpenPrinter(printer_name)
        info = win32print.GetPrinter(handle, 2)

        status = info["Status"]
        attributes = info["Attributes"]

        win32print.ClosePrinter(handle)

        bad_status = (
            win32print.PRINTER_STATUS_ERROR |
            win32print.PRINTER_STATUS_PAPER_OUT |
            win32print.PRINTER_STATUS_PAUSED
        )

        if status & bad_status:
            return False

        if attributes & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE:
            return False

        try:
            dc = win32ui.CreateDC()
            dc.CreatePrinterDC(printer_name)
            dc.DeleteDC()
        except pywintypes.error:
            return False

        return True

    except Exception:
        return False



def is_zebra(printer_name: str) -> bool:
    name = printer_name.lower()
    return "zebra" in name or "zt" in name or "zdesigner" in name
