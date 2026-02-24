import io
import base64
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from typing import List


def render_pdf(pdf_bytes: bytes, dpi: int = 400) -> List[Image.Image]:
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

def render_text(text: str, width: int = 2480, height: int = 3508) -> List[Image.Image]:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except:
        font = ImageFont.load_default()

    margin = 100
    y = margin
    line_height = font.getbbox("Ag")[3] + 10

    for line in text.splitlines():
        draw.text((margin, y), line, fill="black", font=font)
        y += line_height

    return [img]

def render_to_images(payload: dict) -> List[Image.Image]:
    kind = payload.get("kind")
    raw = payload.get("raw")
    encoding = payload.get("encoding")

    if not kind or raw is None:
        raise ValueError("Invalid payload for rendering")

    if encoding == "base64":
        raw = base64.b64decode(raw)

    if kind == "pdf":
        return render_pdf(raw)

    if kind == "text":
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        return render_text(raw)

    if kind == "image":
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        return [img]

    raise ValueError(f"Unsupported render kind: {kind}")
