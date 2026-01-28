# MultiPrint Web Agent 🖨️

<div>
  <img src="https://img.shields.io/badge/PYTHON-3.11.9-blue?style=for-the-badge&logo=python" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/JAVASCRIPT-ES6+-yellow?style=for-the-badge&logo=javascript" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />
  &nbsp;&nbsp;
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
* [Prerequisites](#prerequisites-pushpin)
* [Used Libraries](#used-libraries-books)
* [Architecture](#architecture-building_construction)
* [HTTPS & Self-Signed Certificate](#https--self-signed-certificate-)
* [How to Use](#how-to-use-arrow_forward)
* [API Endpoints](#api-endpoints-link)
* [API Contract](#api-contract-)
* [Roadmap](#roadmap-)
* [Developers & Contributors](#developers--contributors-computer)
* [License](#license-grey_exclamation)
<!--te-->

---

## Project Description :file_folder:

**MultiPrint Web Agent** is a lightweight local printing service designed to bridge **web systems** and **local printers** securely and reliably.

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

## Architecture :building_construction:

- **Flask** backend with Blueprints
- Modular print engines (`print_zebra`, `print_laser`)
- Centralized configuration loader
- Real-time logging via SSE
- Web UI using vanilla JS (ES Modules)
- Secure HTTPS local server

```
MultiPrint_Web-agent/
├── app.py
├── certs/
│   ├── Your localhost self-signed certificate (.crt file)
│   └── Your localhost self-signed key (.key file)
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
└──────────────────────

```

---

# HTTPS & Self-Signed Certificate 🔐

MultiPrint Web Agent **requires HTTPS** to work properly, especially for:
- Browser-based integrations
- JavaScript `fetch` requests
- Secure local communication

Because the agent runs locally, a **self-signed SSL certificate** must be generated for `localhost`.

---

## Why HTTPS is Required

Modern browsers **block insecure (HTTP) requests** when accessing:
- Local APIs
- Printing services
- System-level resources

Running the agent with HTTPS avoids:
- CORS issues
- Mixed content errors
- Browser security blocks

---

## Generating a Self-Signed Certificate (localhost)

Create a `certs/` folder in the project root and generate the certificate:

```bash
mkdir certs

openssl req -x509 -newkey rsa:2048 \
  -keyout certs/localhost.key \
  -out certs/localhost.crt \
  -days 365 \
  -nodes \
  -subj "/CN=localhost"
```

**This will generate:**
* `certs/localhost.crt`
* `certs/localhost.key`

---

## Browser Warning (Expected)

Because the certificate is self-signed, browsers will show a security warning on first access. **This is normal and expected.**

### Steps:
1. Open `https://localhost:<PORT>/ui`
2. Proceed anyway / Trust the certificate

---

## Agent Startup with HTTPS

The agent loads the certificate automatically on startup:

```python
app.run(
    host="127.0.0.1",
    port=AGENT_PORT,
    ssl_context=("certs/localhost.crt", "certs/localhost.key")
)
```

Once running, the UI will display **HTTPS Active**.

---

## How to Use :arrow_forward:

Start the agent:
```bash
python app.py
```

Access the UI:
```
https://localhost:9108/ui
```
> ⚠️ The default port is **9108**.  
> If this port is already in use on your machine, you can change it on config/agent_config.json (agent_port:).

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


 ## API Contract 🧩

The MultiPrint Web Agent exposes a **simple and stable print API** designed to receive **raw print data**, independent of printer type.

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

---

### 🧠 Design Philosophy

- The **client does not need to know** the printer type
- The agent automatically detects whether the printer is Zebra or generic
- This keeps integrations:
  - ✅ Simple  
  - ✅ Stable  
  - ✅ Printer-agnostic  

The `raw` field acts as the **API contract** between external systems and the MultiPrint Web Agent.
        

---

## Roadmap 🧭

### ✅ Phase 1 — Initial Setup
### ✅ Phase 2 — Generic Payload
### ✅ Phase 3 — Printer Configuration
### ✅ Phase 4 — Web UI
### ✅ Phase 5 — UI & UX Refinement
### ✅ Phase 6 — New Features
### ⬜ Phase 7 — Robustness & Security
### ⬜ Phase 8 — Production

---

## Developers & Contributors :computer:

- **Pedro Godoy**
  - [LinkedIn](https://www.linkedin.com/in/pedrogodoy00/)
  - Email: pedro_godoy2@hotmail.com

---

## License :grey_exclamation:

MIT License

Copyright © 2026 — MultiPrint Web Agent
