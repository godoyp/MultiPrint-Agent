import win32print
import win32ui
import pywintypes
from multiprint_agent.core.agent_config import get_thermal_printer, get_laser_printer


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
    

def get_printer_details(printer_name: str) -> dict:

    handle = win32print.OpenPrinter(printer_name)
    info = win32print.GetPrinter(handle, 2)
    win32print.ClosePrinter(handle)

    devmode = info.get("pDevMode")

    return {
        "name": printer_name,
        "driver": info.get("pDriverName"),
        "port": info.get("pPortName"),
        "location": info.get("pLocation") or "N/A",
        "comment": info.get("pComment") or "N/A",
        "orientation": (
            "Portrait" if devmode and devmode.Orientation == 1 else "Landscape"
        ) if devmode else "N/A",
    }


class PrinterNotConfiguredError(RuntimeError):
    pass


def resolve_printer_by_payload(payload: dict) -> str:

    kind = payload.get("kind")

    if kind == "zpl":
        printer = get_thermal_printer()
        if not printer:
            raise PrinterNotConfiguredError(
                "Thermal printer not configured"
            )
        return printer

    printer = get_laser_printer()
    if not printer:
        raise PrinterNotConfiguredError(
            "Laser printer not configured"
        )
    return printer
