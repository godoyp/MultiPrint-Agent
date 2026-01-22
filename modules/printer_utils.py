# CHECK PRINTER MODEL (ZEBRA OR LASER)

def is_zebra(printer_name: str) -> bool:
    name = printer_name.lower()
    return "zebra" in name or "zt" in name or "zdesigner" in name
