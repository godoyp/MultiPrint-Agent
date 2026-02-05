# MultiPrint Web Agent 🖨️


<div>
  <img src="https://img.shields.io/badge/PYTHON-3.11.9-blue?style=for-the-badge&logo=python" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/JAVASCRIPT-ES6+-yellow?style=for-the-badge&logo=javascript" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />
</div>
<div>
  <img src="https://img.shields.io/badge/HTTPS-Local%20Secure-success?style=for-the-badge" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/STATUS-Active-success?style=for-the-badge" />
</div>

---

# Language: 
🇺🇸 English | 🇧🇷 [Português](README_PT-Br.md)

---

**MultiPrint Web Agent** is a local printing agent that exposes a **simple HTTP API** for integration with external systems, abstracting the complexity of printer drivers, printer types, and the operating system.

It allows any application to send print jobs via HTTP, while the agent handles security, validation, and dispatching to **laser** or **thermal (Zebra)** printers.

This project is ideal for systems that need to **print locally** without dealing directly with:
- printer drivers
- operating system spoolers
- differences between laser and thermal printers

---

## ✨ Key Features

- 🖨️ Support for **Laser** and **Thermal (ZPL / Zebra)** printers
- 🌐 Simple and predictable HTTP API
- 🔐 Security with **session tokens**
- 🚦 Per-route rate limiting
- 🧠 Payload detection and validation
- 📊 Agent state available via API
- 🧪 Local UI for configuration and diagnostics
- 🧱 Modular and extensible architecture

---

## 🏗️ Overview

```
External Client
      ↓
MultiPrint Web Agent
      ↓
System Printers (Laser / Thermal)
```

The client **never communicates directly with the printer**.  
All validation, decision-making, and dispatch logic happens inside the agent.

> ⚠️ The agent’s default port is **9108**.  
> If this port is already in use on your machine, you can change it in  
> `config/agent.json` by adjusting the `agent_port` property.

---

## 🔐 Why HTTPS Is Required

Modern browsers **block insecure (HTTP) requests** when accessing:
- Local APIs
- Printing services
- System-level resources

Running the agent using **HTTPS** avoids:
- CORS issues
- Mixed content errors
- Browser security blocks

> ⚠️ The SSL certificate used is **self-signed** and **automatically generated during the agent installation process**.

---

## 🌐 Browser Warning (Expected)

Because the SSL certificate is **self-signed**, the browser will display a **security warning on first access**.  
**This behavior is normal and expected.**

### Steps:
1. Open `https://localhost:<PORT>/ui`
2. Choose **Advanced** / **Proceed anyway**
3. Confirm trust for the certificate

After this, the warning will no longer appear for the same browser.

---

## 🧠 Design Philosophy

MultiPrint Web Agent is designed to **simplify integrations** and **isolate printing complexity** from the client side.

Core principles:

- The **client does not need to know** the printer type
- The agent automatically detects whether the printer is:
  - thermal (Zebra / ZPL)
  - or generic (laser)
- Hardware-specific logic is **centralized in the agent**, not spread across client systems

This ensures integrations that are:
- ✅ Simple  
- ✅ Stable  
- ✅ Printer-agnostic  

The `raw` field acts as the **API contract** between external systems and the MultiPrint Web Agent, allowing clients to send data without needing to understand rendering details, drivers, or OS-level spooling.

This model reduces coupling, simplifies maintenance, and allows the printing environment to evolve without impacting existing integrations.

## ❌ What This Project Is Not

To clearly define scope, MultiPrint Web Agent:

- ❌ Is not a cloud printing service
- ❌ Does not expose printers directly to the network
- ❌ Does not replace operating system drivers
- ❌ Does not require clients to understand hardware details

The goal of the project is to **centralize and abstract local printing complexity**, keeping integrations simple and stable.

---

## 📦 Print Payload

The `/print` endpoint accepts a flexible payload.  
The only **required** field is `raw`.

Additional fields are **optional**, but they **help the agent identify the payload type more accurately**, making processing more reliable.

### Supported fields

| Field         | Required | Description |
|---------------|----------|-------------|
| `raw`         | ✅ Yes   | Raw content to be printed |
| `contentType` | ❌ No    | MIME type of the content (e.g. `application/pdf`) |
| `encoding`    | ❌ No    | Payload encoding (e.g. `base64`) |

---

### 🔍 How the agent detects the payload

The agent uses a combination of **content inspection** and **auxiliary metadata**:

- **ZPL**
  - Automatically detected by the presence of `^XA` and `^XZ` commands
  - Does not require `contentType` or `encoding`

- **PDF**
  - Identified by:
    - `contentType: application/pdf`
    - or `%PDF` signature after base64 decoding

- **Images**
  - Identified by binary signatures (PNG or JPEG) after base64 decoding

- **Text**
  - Used as a fallback when no specific pattern is detected

Fields such as `contentType` and `encoding` are **not mandatory**, but help the agent make more accurate decisions in ambiguous scenarios.

---

## 🔌 API – Main Endpoints

### 🔐 POST /auth/handshake

Creates a session and returns a **session token**.

```json
{
  "token": "SESSION_TOKEN",
  "expires_in": 1800
}
```

---

### 🖨️ POST /print

Sends a print job.

**Headers**
```
Authorization: Bearer <SESSION_TOKEN>
Content-Type: application/json
```

**Body (ZPL example)**
```json
{
  "raw": "^XA^FO50,50^FDHello World^FS^XZ"
}
```

---

### 📊 GET /state

Returns the current agent state.

```json
{
  "status": "online",
  "printers": {
    "laser": "HP LaserJet",
    "thermal": "Zebra ZT230"
  },
  "port": 9108,
  "version": "1.0.0"
}
```

---

## 🚀 Integration Example (JavaScript)

```js
async function getToken(forceRenew = false) {
  if (!window.cachedToken || forceRenew) {
    const res = await fetch("https://localhost:9108/auth/handshake", {
      method: "POST"
    });
    const { token } = await res.json();
    window.cachedToken = token;
  }
  return window.cachedToken;
}

async function printPayload(payload) {
  let token = await getToken();

  let res = await fetch("https://localhost:9108/print", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify(payload)
  });

  // Token expired → renew and retry
  if (res.status === 401) {
    token = await getToken(true);
    res = await fetch("https://localhost:9108/print", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify(payload)
    });
  }

  if (!res.ok) {
    throw new Error("Print failed");
  }
}

// ZPL example (auxiliary fields not required)
printPayload({
  raw: "^XA^FO50,50^FDHello World^FS^XZ"
});

// PDF example (base64 + auxiliary metadata)
printPayload({
  raw: pdfBase64,
  encoding: "base64",
  contentType: "application/pdf"
});

// Image example (PNG/JPEG in base64)
printPayload({
  raw: imageBase64,
  encoding: "base64",
  contentType: "image/png"
});
```

---

## 🧪 Local UI (Configuration)

The agent includes a **local UI** used only for:

- Listing system printers
- Classifying printers (laser / thermal)
- Selecting printers by role
- Running test prints
- Viewing logs
- Checking agent state

> ⚠️ The UI **is not part of the external integration**  
> It exists only for local setup and diagnostics.

---

## 🔐 Security

- Session tokens required for protected routes
- Per-route rate limiting
- Handshake restricted to the local environment
- Tokens automatically renewable by the client when expired

The sections below describe how security is configured and enforced.

## 🔐 Security Configuration

The MultiPrint Web Agent separates **secrets** from **behavioral security settings**.

This ensures a secure setup while keeping the system easy to configure across different environments.

### Environment Variable (Required)

The API key used to authenticate external clients **must be provided via environment variable**.

This value is considered sensitive and **must not be stored in configuration files or version control**.

#### Required variable

- `MULTIPRINT_API_KEY`  
  API key used by external systems to authenticate print requests.

If this variable is not set, the agent will **fail to start**.

### Session TTL Configuration

The session expiration time is configurable via the `security.json` file.

This setting defines how long a session token remains valid after being issued.

```json
{
  "session_ttl": 1800 // 30 minutes
}
```

- The value is expressed in **seconds**
- This file contains **non-sensitive configuration**
- It is safe to keep it under version control
- If the file or value is missing, a safe default is used

### How Session Expiration Works

- The session TTL is loaded from `security.json`
- The value is applied during `/auth/handshake`
- Each issued token receives its own expiration timestamp
- Expired tokens are automatically invalidated

This design keeps session policy explicit, configurable, and isolated from core security bootstrap logic.

### Design Rationale

- **Secrets** (API keys) are loaded from environment variables
- **Security behavior** (such as session lifetime) is loaded from configuration files
- **Session logic** remains stateless and policy-agnostic

This separation avoids accidental secret exposure while keeping the agent flexible across environments.

---

## 🏗️ Architecture

MultiPrint Web Agent is designed with a focus on **modularity**, **clear responsibilities**, and **ease of evolution**.

> ℹ️ Currently, the agent is focused on **Windows** environments due to direct integration with the OS printing subsystem.

### 🔧 Technical overview

- **Flask** backend organized with **Blueprints**
- Modular print engines:
  - `print_zebra` (thermal / ZPL printing)
  - `print_laser` (generic / OS printing)
- Centralized configuration loading
- Real-time logs via **SSE (Server-Sent Events)**
- Local Web UI built with **JavaScript ES6+ (ES Modules)**
- Local server running with **HTTPS** and a self-signed certificate

### 🧠 Internal architecture (by responsibility)

The codebase is organized into well-defined domains:

- **security**  
  Authentication, sessions, rate limiting, and access control

- **payload**  
  Detection, normalization, and validation of print data

- **printers**  
  Printer detection, status checks, and classification

- **printing**  
  Rendering and dispatching print jobs to the OS

- **observability**  
  Logs, events, and diagnostics

- **core**  
  Central configuration and agent runtime state

This separation ensures low coupling, easier testing, and future evolution without breaking existing integrations.

---

## ⚙️ Configuration Files and Certificates

For security reasons, some files are **not versioned in the repository**:

- `certs/`  
  Contains the SSL certificate and private key used by the agent.

- `config/security.json`  
  Contains sensitive security-related configuration for the agent.

These files are **automatically generated during the agent installation process**.

### Manual execution (development environment)

If the agent is executed directly via Python, you must ensure that:

- the `certs/` directory exists
- the `config/security.json` file is present

The repository includes **example configuration files** that can be used as a starting point:

- `config/security.example.json`

These files should be copied and adjusted locally before running the agent.

---

## 📦 Project Status

**Current version:** `v1.0.0`

✔️ Architecture consolidated  
✔️ Well-defined flows  
✔️ Ready for local production use  

---

## 🧭 Roadmap

### ✅ Phase 1 — Initial Setup
Base agent structure, project setup, and server bootstrap.

### ✅ Phase 2 — Generic Payload
Support for multiple payload types (ZPL, PDF, images) with automatic detection.

### ✅ Phase 3 — Printer Configuration
Selection and persistence of laser and thermal printers.

### ✅ Phase 4 — Web UI
Creation of the local UI for configuration and diagnostics.

### ✅ Phase 5 — UI & UX Refinement
Visual improvements, feedback, states, and user experience.

### ✅ Phase 6 — New Features
Test print, logs, printer classification, and additional capabilities.

### ✅ Phase 7 — Robustness & Security
Session tokens, rate limiting, validation, failure handling, and hardening.

### ⬜ Phase 8 — Production
Final packaging, complete documentation, and production readiness.

---

## 📝 License

MIT License

Copyright © 2026 — MultiPrint Web Agent
