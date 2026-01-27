# LocalPrint Agent 🖨️

<div>
  <img src="https://img.shields.io/badge/PYTHON-3.9%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/STATUS-Active-success?style=for-the-badge" />
</div>

<h4>
	Project status: Actively developed 🚀
</h4>

---

## Topics :writing_hand:
<!--ts-->
* [Project Description](#project-description-file_folder)
* [Features](#features-gear)
* [Architecture](#architecture-bricks)
* [Requirements](#requirements-pushpin)
* [Configuration](#configuration-wrench)
* [How to Use](#how-to-use-arrow_forward)
* [Libraries Used](#libraries-used-books)
* [Notes](#notes-eyes)
* [Screenshot](#screenshot-camera)
* [Developers and Contributors](#developers-and-contributors-computer)
* [License](#license-grey_exclamation)
<!--te-->

---

## Project Description :file_folder:
**LocalPrint Agent** is a local printing agent written in Python that allows applications to send print jobs directly to printers installed on the machine, without requiring drivers on the client system.

It is designed to run as a **secure local service**, exposing a **HTTPS API**, a **web dashboard**, **real-time logs**, and support for multiple printer types.

Ideal use cases:
- ERP integrations
- Web systems
- Industrial environments
- Controlled local printing via API

---

## Features :gear:
<div>✅ Print via REST API (`/print`)</div>
<p></p>
<div>✅ Zebra printer support (ZPL)</div>
<p></p>
<div>✅ Generic / laser printer support (TEXT)</div>
<p></p>
<div>✅ Print test directly from the UI</div>
<p></p>
<div>✅ Local web interface (dashboard)</div>
<p></p>
<div>✅ Select and switch active printer</div>
<p></p>
<div>✅ Real-time logs via SSE</div>
<p></p>
<div>✅ Offline printer validation</div>
<p></p>
<div>✅ HTTPS with self-signed certificate</div>
<p></p>
<div>✅ Fully modularized backend and frontend</div>

---

## Architecture :bricks:
- **Backend**
  - Flask with Blueprints
  - Core modules for configuration and state
  - Smart print dispatcher by printer type
- **Frontend**
  - Lightweight and professional web UI
  - Modular JavaScript (ES Modules)
  - Real-time logs via EventSource (SSE)
- **Infrastructure**
  - Local HTTPS
  - Persistent JSON-based configuration
  - File logs + streaming logs

---

## Requirements :pushpin:
<div><b>:warning: REQUIRED :warning:</b> Windows environment</div>
<p></p>

- Python 3.9+
- Printers installed on the system
- Local SSL certificate (self-signed)

Install dependencies:
```bash
pip install flask flask-cors pywin32
