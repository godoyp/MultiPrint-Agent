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
localprint-agent/
├── app.py
├── certs/
│   ├── Your localhost self-signed certificate
│   └── Your localhost self-signed key
├── config/
│   ├── config.json
│   └── zebra_printers.json
├── core/
│   ├── agent_config.py
│   ├── dispatcher.py
│   └── printer_state.py
├── logs/
│   └── agent.log
├── modules/
│   ├── eventlog.py
│   ├── print_laser.py
│   ├── print_zebra.py
│   └── printer_utils.py
├── routes/
│   ├── config.py
│   ├── health.py
│   ├── logs.py
│   ├── print.py
│   ├── print_test.py
│   ├── printers.py
│   ├── ui.py
│   └── version.py
├── static/
│   ├── ui.html
│   ├── css/
│   │   └── ui.css
│   ├── images/
│   │   └── logo.png
│   └── js/
│       ├── api.js
│       ├── init.js
│       ├── logs.js
│       ├── printers.js
│       ├── status.js
│       └── toasts.js

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

JavaScript implementation exemple:
```javascript
fetch("https://localhost:9108/print", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    raw: "YOUR_PAYLOAD_HERE" // 👈 Replace with your ZPL / RAW / TEXT payload
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));

```

 ## API Contract 🧩

The LocalPrint Agent exposes a **simple and stable print API** designed to receive **raw print data**, independent of printer type.

### 🔹 Endpoint

```
POST /print
```

### 🔹 Request Body

The request **must** be a JSON object containing the `raw` field.

```json
{
  "raw": "<RAW_PRINT_PAYLOAD>"
}
```

### 🔹 `raw` Field

- `raw` represents the **raw print payload**
- It is sent **exactly as received** to the configured printer
- Supported formats depend on the printer type:
  - **Zebra printers** → ZPL
  - **Generic / Laser printers** → Plain text
  - (Future) ESC/POS, queued jobs, retries, etc.

> ⚠️ The key name **must be `raw`**.  
> If the field is missing or empty, the agent will reject the request with an error.

---

### 🔹 Example (JavaScript)

```javascript
fetch("https://localhost:5000/print", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    raw: "^XA^FO50,50^FDHello World^FS^XZ"
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
```

---

### 🧠 Design Philosophy

- The **client does not need to know** the printer type
- The agent automatically detects whether the printer is Zebra or generic
- This keeps integrations:
  - ✅ Simple  
  - ✅ Stable  
  - ✅ Printer-agnostic  

The `raw` field acts as the **API contract** between external systems and the LocalPrint Agent.

            

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
