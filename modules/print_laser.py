import win32print
import win32ui
import win32con
from PIL import ImageWin


def print_laser(printer_name: str, images):
    hPrinter = win32print.OpenPrinter(printer_name)

    try:
        devmode = win32print.GetPrinter(hPrinter, 2)["pDevMode"]
        devmode.Orientation = win32con.DMORIENT_PORTRAIT

        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)

        hdc.StartDoc("Laser Print")

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

    finally:
        win32print.ClosePrinter(hPrinter)
