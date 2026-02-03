import base64
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black, grey
from reportlab.lib.utils import ImageReader
from modules.printers.utils import get_printer_details


def generate_laser_test_pdf_base64(printer_name: str) -> str:

    printer = get_printer_details(printer_name)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFillColor(black)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, "static", "images", "logo.png")

    logo_width = 18 * mm
    logo_height = 18 * mm

    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(
            logo,
            20 * mm,
            height - 28 * mm,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )
    else:
        c.rect(20 * mm, height - 25 * mm, 12 * mm, 12 * mm, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(
        42 * mm,
        height - 18 * mm,
        "MultiPrint Web Agent"
    )

    c.setFont("Helvetica", 11)
    c.drawString(
        42 * mm,
        height - 25 * mm,
        "Print Test — Laser Printer"
    )

    c.setStrokeColor(grey)
    c.setLineWidth(0.7)
    c.line(
        20 * mm,
        height - 32 * mm,
        width - 20 * mm,
        height - 32 * mm
    )

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(
        20 * mm,
        height - 55 * mm,
        "Print completed successfully ✔"
    )

    y = height - 80 * mm
    line_height = 18

    c.setFont("Helvetica-Bold", 13)
    c.drawString(20 * mm, y, "Details")

    y -= line_height * 2

    c.setFont("Helvetica", 11)

    def draw_detail(label: str, value: str):
        nonlocal y
        c.drawString(25 * mm, y, f"• {label}: {value}")
        y -= line_height

    draw_detail("Printer name", printer.get("name", "N/A"))
    draw_detail("Printer type", "Laser")
    draw_detail("Driver", printer.get("driver", "N/A"))
    draw_detail("Port", printer.get("port", "N/A"))
    draw_detail("Location", printer.get("location", "N/A"))
    draw_detail("Comment", printer.get("comment", "N/A"))
    draw_detail("Orientation", printer.get("orientation", "N/A"))
    draw_detail("Print payload", "PDF (base64)")
    draw_detail("Processing pipeline", "PDF → Image → GDI")
    draw_detail("Rendering engine", "Internal (PyMuPDF)")
    draw_detail("External software", "None")
    draw_detail("Compatibility", "Windows Print Spooler")

    c.setFont("Helvetica", 9)
    c.setFillColor(grey)

    c.drawString(
        20 * mm,
        18 * mm,
        "MultiPrint Web Agent — Test page"
    )

    c.drawRightString(
        width - 20 * mm,
        18 * mm,
        "Powered by Python"
    )

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return base64.b64encode(pdf_bytes).decode("utf-8")

def generate_thermal_test_zpl():

    zpl_payload = (
                    "^XA\r\n"
                    "^PW800\r\n"
                    "^LL480\r\n"
                    "^FO40,30^A0N,50,50^FDPRINT TEST^FS\r\n"
                    "^FO40,90^A0N,30,30^FDMultiPrint Web Agent^FS\r\n"
                    "^FO500,40^BQN,2,10^FDLA,PRINT-TEST-OK^FS\r\n"
                    "^XZ\r\n"
                )

    return zpl_payload
