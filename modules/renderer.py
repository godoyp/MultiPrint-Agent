import fitz  # PyMuPDF
from PIL import Image
from typing import List
import io


def render_pdf(pdf_bytes: bytes, dpi: int = 300) -> List[Image.Image]:

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    images = []

    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        images.append(img)

    doc.close()
    return images
