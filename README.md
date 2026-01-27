# LocalPrint Agent 🖨️

<div>
  <img src="https://img.shields.io/badge/PYTHON-3.11.9-blue?style=for-the-badge&logo=python" />
</div>
<div>
  <img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />
</div>
<div>
  <img src="https://img.shields.io/badge/STATUS-Active-success?style=for-the-badge" />
</div>

<h4>
  Project Status: Active Development ✅
</h4>

Topics :writing_hand:
====================
<!--ts-->
* [Project Description](#project-description-file_folder)
* [Features](#features-gear)
* [Architecture](#architecture-building_construction)
* [Prerequisites](#prerequisites-pushpin)
* [Used Libraries](#used-libraries-books)
* [How to Use](#how-to-use-arrow_forward)
* [API Endpoints](#api-endpoints-link)
* [Roadmap](#roadmap-map)
* [Developers & Contributors](#developers--contributors-computer)
* [License](#license-grey_exclamation)
<!--te-->

---

## Project Description :file_folder:

**LocalPrint Agent** is a lightweight local printing service designed to bridge **web systems** and **local printers** securely and reliably.

It runs locally on Windows, exposes a secure HTTPS API, and allows applications to send **raw print payloads** directly to printers such as **Zebra (ZPL)**, **laser**, and future **ESC/POS** devices.

---

## Features :gear:

✔ Raw print endpoint (`/print`)  
✔ Zebra printers support (ZPL)  
✔ Generic / Laser printers support  
✔ Printer selection and persistence  
✔ Web UI dashboard  
✔ Real-time logs via **SSE (Server-Sent Events)**  
✔ HTTPS with self-signed certificate  
✔ Modular backend and frontend architecture  

---

## Architecture :building_construction:

- **Flask** backend with Blueprints
- Modular print engines (`print_zebra`, `print_laser`)
- Centralized configuration loader
- Real-time logging via SSE
- Web UI using vanilla JS (ES Modules)
- Secure HTTPS local server

```
project-root/
├── app.py
├── core/
│   └── agent_config.py
├── routes/
├── modules/
│   ├── eventlog.py
│   ├── print_zebra.py
│   ├── print_laser.py
│   └── printer_utils.py
├── static/
│   ├── ui.html
│   ├── ui.css
│   └── js/
│       └── ui.js
├── config/
│   ├── config.json
│   └── zebra_printers.json
└── logs/
```

---

## Prerequisites :pushpin:

- Windows OS
- Python **3.11.9**
- Printer drivers installed locally
- HTTPS certificates generated (self-signed)

Install dependencies:
```bash
pip install flask flask-cors pywin32
```

---

## Used Libraries :books:

- [Flask](https://pypi.org/project/Flask/)
- [Flask-CORS](https://pypi.org/project/flask-cors/)
- [pywin32](https://pypi.org/project/pywin32/)
- Python Standard Library

---

## How to Use :arrow_forward:

Start the agent:
```bash
python app.py
```

Access the UI:
```
https://localhost:5000/ui
```

Send a print job:
```http
POST /print
Content-Type: application/json

{
  "raw": "^XA^FO50,50^FDHello World^FS^XZ"
}
```

---

## API Endpoints :link:

- `POST /print` — Send raw payload to printer
- `POST /test-print` — Test printer
- `GET /printers` — List printers
- `POST /config/printer` — Set active printer
- `GET /health` — Agent status
- `GET /logs/stream` — Real-time logs (SSE)
- `GET /version` — Agent version

---

## Roadmap :map:

### ✅ Phase 1 — Initial Setup
### ✅ Phase 2 — Generic Payload
### ✅ Phase 3 — Printer Configuration
### ✅ Phase 4 — Web UI
### ✅ Phase 5 — UI & UX Refinement
### ⬜ Phase 6 — Robustness & Security
### ⬜ Phase 7 — Advanced Features

---

## Developers & Contributors :computer:

- **Pedro Godoy**
  - [LinkedIn](https://www.linkedin.com/in/pedrogodoy00/)
  - Email: pedro_godoy2@hotmail.com

---

## License :grey_exclamation:

MIT License

Copyright © 2026 — LocalPrint Agent
