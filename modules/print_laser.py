import win32print
import win32ui
import win32con
from PIL import ImageWin


def print_laser_image(printer_name: str, images):
    hPrinter = win32print.OpenPrinter(printer_name)
    devmode = win32print.GetPrinter(hPrinter, 2)["pDevMode"]
    devmode.Orientation = win32con.DMORIENT_PORTRAIT

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    hdc.StartDoc("Laser Image Print")

    printable_width = hdc.GetDeviceCaps(win32con.HORZRES)
    printable_height = hdc.GetDeviceCaps(win32con.VERTRES)

    for img in images:
        hdc.StartPage()

        img_width, img_height = img.size

        scale = min(
            printable_width / img_width,
            printable_height / img_height
        )

        draw_width = int(img_width * scale)
        draw_height = int(img_height * scale)

        x = (printable_width - draw_width) // 2
        y = (printable_height - draw_height) // 2

        dib = ImageWin.Dib(img)
        dib.draw(
            hdc.GetHandleOutput(),
            (x, y, x + draw_width, y + draw_height)
        )

        hdc.EndPage()

    hdc.EndDoc()
    hdc.DeleteDC()
    win32print.ClosePrinter(hPrinter)


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
