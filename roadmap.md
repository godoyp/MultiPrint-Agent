# 🧭 Roadmap — MultiPrint Web Agent

This document describes the **official evolution plan** of the **MultiPrint Web Agent** project, detailing phases, goals, and delivered or planned features.

> 📌 **This is the official project roadmap**  
> Any changes should be intentional and versioned.

---

## 🖥️ PHASE 1 — Initial Setup ✅

🎯 **Goal:** Prepare the environment and ensure secure local execution

### Deliverables
- ✅ Create basic Python agent using Flask
- ✅ Configure localhost execution
- ✅ Generate and configure self-signed SSL certificate
- ✅ Basic ZPL print test on Zebra printer

---

## 🖥️ PHASE 2 — Generic Payload ✅

🎯 **Goal:** Accept any raw payload for printing

### Deliverables
- ✅ `POST /print` endpoint with `raw` payload
- ✅ Zebra printer support (ZPL)
- ✅ Generic / laser printer support (TEXT)
- ✅ Modular backend architecture:
  - `print_zebra.py`
  - `print_laser.py`
- ✅ Centralized event logging (`eventlog.py`)

---

## 🖥️ PHASE 3 — Printer Configuration ✅

🎯 **Goal:** Select, persist, and manage local printers

### Deliverables
- ✅ List available printers (`GET /printers`)
- ✅ Printer selection via Web UI
- ✅ Persist selected printer in `config.json`
- ✅ `POST /config/printer` endpoint
- ✅ Agent state endpoint (`GET /state`)
- ✅ Test print endpoint (`POST /test-print`) for:
  - Zebra printers
  - Generic printers

---

## 🖥️ PHASE 4 — Web UI ✅

🎯 **Goal:** Provide a clear and professional web interface

### Deliverables
- ✅ Agent status dashboard
- ✅ Active printer display
- ✅ Printer selection and switching via UI
- ✅ Print test button
- ✅ Visual feedback (toasts)
- ✅ Responsive layout (status + logs side by side)
- ✅ Real-time logs via **SSE**
- ✅ Visible agent port
- ✅ Clean, mini-dashboard layout

---

## 🖥️ PHASE 5 — UI & UX Refinement ✅ **(COMPLETED)**

🎯 **Goal:** Deliver a usable, robust, and professional product

### State & UX
- ✅ Agent online/offline status
- ✅ Active printer updated in real time
- ✅ Toast-based feedback
- ✅ Clear visual error messages

### Observability
- ✅ Real-time logs via SSE
- ✅ Last executed action
- ✅ Event timestamps

### Printers
- ✅ “Reload printers” button
- ✅ Log when reloading printers
- ✅ Log when saving selected printer
- ✅ Offline printer validation before printing

### Security & Infra
- ✅ HTTPS active indicator
- ✅ Visible port with copy option
- ✅ Self-signed certificate warning

### Product
- ✅ Agent version displayed in UI (`GET /version`)
- ✅ Organized mini-dashboard

### Architecture
- ✅ Modular UI (JavaScript ES Modules)
- ✅ Clean, decoupled backend architecture (core / routes / modules)

---

## 🧩 PHASE 6 — New Features ⏳

🎯 **Goal:** Expand agent capabilities

### Planned
- ⬜ PDF support for laser printers
- ⬜ Multiple printer selection (thermal and laser)

---

## 🛡️ PHASE 7 — Robustness & Security ⏳

🎯 **Goal:** Prepare the agent for more critical environments

### Planned
- ⬜ API token authentication
- ⬜ Payload validation
- ⬜ Rate limiting
- ⬜ HTTPS hardening and validation
- ⬜ Advanced logging
- ⬜ Automatic print retry / fallback
- ⬜ Critical error notifications (optional)

---

## 🧩 PHASE 8 — Production ⏳

🎯 **Goal:** Packaging and distribution

### Planned
- ⬜ External service integrations
- ⬜ Packaging as **Windows EXE**
- ⬜ EXE running in **system tray**

---

## 📌 Final Notes

- The project follows a **printer-agnostic** philosophy
- The API contract is based on **raw payload (`raw`)**
- UI and backend are fully decoupled
- This document is the **single source of truth** for project planning

---

📅 **Last update:** 2026  
🖨️ **Project:** MultiPrint Web Agent
