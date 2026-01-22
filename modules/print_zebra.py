import win32print

def print_zebra(printer_name: str, raw_zpl: str):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        win32print.StartDocPrinter(
            hPrinter, 1, ("ZPL Print", None, "RAW")
        )
        win32print.StartPagePrinter(hPrinter)

        # Zebra = ASCII + CRLF
        data = raw_zpl.replace("\n", "\r\n").encode("ascii", errors="ignore")
        win32print.WritePrinter(hPrinter, data)

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
