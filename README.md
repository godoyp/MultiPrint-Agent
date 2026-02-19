<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/multiprint_web_agent/static/images/logo-white.png">
    <source media="(prefers-color-scheme: light)" srcset="/multiprint_web_agent/static/images/logo.png">
    <img src="/multiprint_web_agent/static/images/logo-white.png" width="150">
  </picture>
</p>

<h1 align="center">MultiPrint Web Agent</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11.9-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/JavaScript-ES6+-C9A227?style=for-the-badge&logo=javascript&logoColor=white" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" />
</div>
<br>
<div align="center">
  <img src="https://img.shields.io/badge/Poetry-Packaging%20%26%20Build-6F42C1?style=for-the-badge&logo=python&logoColor=white" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/PyInstaller-Executable%20Build-F37626?style=for-the-badge" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/HTTPS-Local%20Secure-2E8B57?style=for-the-badge" />
</div>
<br>
<div align="center">
  <img src="https://img.shields.io/badge/License-MIT-1E90FF?style=for-the-badge" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Status-Active-2E8B57?style=for-the-badge" />
</div>

## Language: 
🇺🇸 English | 🇧🇷 [Português](README_PT-Br.md)

---

**MultiPrint Web Agent** is a local printing agent that exposes a **simple HTTP API** for integration with external systems, abstracting the complexity of printer drivers, printer types, and the operating system.

It allows any application to send print jobs via HTTP, while the agent handles security, validation, and dispatching to **laser** or **thermal (Zebra)** printers.

This project is ideal for systems that need to **print locally** without dealing directly with:
- printer drivers
- operating system spoolers
- differences between laser and thermal printers

---

## 📑 Table of Contents

- [✨ Key Features](#-key-features)
- [🏗️ Overview](#️-overview)
- [🔐 Why HTTPS Is Required](#-why-https-is-required)
- [🌐 Browser Warning (Expected)](#-browser-warning-expected)
- [🧠 Design Philosophy](#-design-philosophy)
- [❌ What This Project Is Not](#-what-this-project-is-not)
- [📦 Print Payload](#-print-payload)
- [🔌 API – Main Endpoints](#-api--main-endpoints)
- [🚀 Integration Example (JavaScript)](#-integration-example-javascript)
- [🧪 Local UI (Configuration)](#-local-ui-configuration)
- [🏗️ Architecture](#️-architecture)
- [🔐 Security](#-security)
- [🧪 Development Setup (Manual Execution)](#-development-setup-manual-execution)
- [🛠️ Poetry](#️-poetry)
- [📦 Project Status](#-project-status)
- [📝 License](#-license)

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

The `/api/print` endpoint accepts a flexible payload.  
The only **required** field is `raw`.

Additional fields are **optional**, but they **help the agent identify the payload type more accurately**, making processing more reliable.

### Supported fields

| Field         | Required | Description |
|---------------|----------|-------------|
| `raw`         | ✅ Yes   | Raw content to be printed |
| `contentType` | ❌ No    | MIME type of the content (e.g. `application/pdf`) |
| `encoding`    | ❌ No    | Payload encoding (e.g. `base64`) |


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

### 🔐 POST /api/auth/handshake

Creates a session and returns a **session token**.

```json
{
  "token": "SESSION_TOKEN",
  "expires_in": 1800
}
```


### 🖨️ POST /api/print

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

## 🚀 Integration Example (JavaScript)

```js
async function getToken(forceRenew = false) {
  if (!window.cachedToken || forceRenew) {
    const res = await fetch("https://localhost:9108/api/auth/handshake", {
      method: "POST"
    });
    const { token } = await res.json();
    window.cachedToken = token;
  }
  return window.cachedToken;
}

async function printPayload(payload) {
  let token = await getToken();

  let res = await fetch("https://localhost:9108/api/print", {
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
    res = await fetch("https://localhost:9108/api/print", {
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

<p align="center">
  <img src="/multiprint_web_agent/static/images/MultiPrint.png">
</p>

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

## 🔐 Security

- Session tokens required for protected routes
- Per-route rate limiting
- Handshake restricted to the local environment
- Tokens automatically renewable by the client when expired

The sections below describe how security is configured and enforced.

### Security Configuration

The MultiPrint Web Agent separates **secrets** from **behavioral security settings**.

This ensures a secure setup while keeping the system easy to configure across different environments.

### Environment Variable

The API key used to authenticate external clients **is provided via environment variable and is generated during the installation process**.

This value is considered sensitive and **must not be stored in configuration files or version control**.

### Required variable

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

### Certificate

For security reasons, some files are **not versioned in the
repository**:

-   `certs/`\
    Contains the SSL certificate (`.crt`) and private key (`.key`) used
    by the agent.

**These files are generated during the installation process of the agent.**

---

## 🧪 Development Setup (Manual Execution)

When running the agent directly via Python (development mode), you must
manually ensure that:

-   the `certs/` directory exists\
-   the SSL certificate and private key are present\
-   the API-KEY is set as a Environment Variable `MULTIPRINT_API_KEY`  

### 🔐 Generating a Localhost SSL Certificate (Development Only)

For development environments, you must manually generate a **self-signed
certificate** for `localhost`.

### Step 1 --- Install OpenSSL

Make sure OpenSSL is installed and available in your system PATH.

To verify:

``` bash
openssl version
```

If the command is not recognized, install OpenSSL and restart your
terminal.

### Step 2 --- Create the `certs` directory

Inside the project root:

``` bash
mkdir certs
```

### Step 3 --- Generate the certificate and key

Run the following command inside the project root:

``` bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/agent.key -out certs/agent.crt -days 365 -subj "/CN=localhost"
```

This will generate:

-   `certs/agent.key`
-   `certs/agent.crt`

The certificate will be valid for **365 days**.

### Set the API Key

#### PowerShell

``` powershell
setx MULTIPRINT_API_KEY "mp_dev_your_generated_key_here"
```

### 🛠️ Poetry

MultiPrint Web Agent uses **Poetry** for dependency management and
packaging.

### Requirements

-   Python 3.11+
-   Poetry installed

### Install Poetryper

If Poetry is not installed:

``` bash
pip install poetry
```

Or follow the official instructions:\
https://python-poetry.org/docs/

### Install Dependencies

Inside the project root:

``` bash
poetry install
```

### Run the Agent (Development Mode)

``` bash
poetry run python -m multiprint_web_agent.app
```

The agent will start using HTTPS on the configured port.

### Adding New Dependencies

To add a runtime dependency:

``` bash
poetry add <package-name>
```

To add a development-only dependency:

``` bash
poetry add --group dev <package-name>
```

### Dependency File

All dependencies are defined in:

`pyproject.toml`

There is no `requirements.txt` file in this project.

---

## 📦 Project Status

**Current version:** `v0.1.0`

✔️ Stable local execution  
✔️ Executable distribution (PyInstaller)  
✔️ HTTPS-secured communication  
🚧 REST architecture evolution in progress  

---

## 📝 License

MIT License

Copyright © 2026 — Pedro Godoy - MultiPrint Web Agent
