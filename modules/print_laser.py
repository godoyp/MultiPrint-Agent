import win32print

def print_laser(printer_name: str, text: str):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        win32print.StartDocPrinter(
            hPrinter, 1, ("Laser Print", None, "TEXT")
        )
        win32print.StartPagePrinter(hPrinter)

        win32print.WritePrinter(hPrinter, text.encode("utf-8"))

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
