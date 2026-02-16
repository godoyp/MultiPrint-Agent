```{=html}
<p align="center">
```
`<picture>`{=html}
`<source media="(prefers-color-scheme: dark)" srcset="/multiprint_web_agent/static/images/logo-white.png">`{=html}
`<source media="(prefers-color-scheme: light)" srcset="/multiprint_web_agent/static/images/logo.png">`{=html}
`<img src="/multiprint_web_agent/static/images/logo-white.png" width="150">`{=html}
`</picture>`{=html}
```{=html}
</p>
```
```{=html}
<h1 align="center">
```
MultiPrint Web Agent
```{=html}
</h1>
```
::: {align="center"}
`<img src="https://img.shields.io/badge/PYTHON-3.11.9-blue?style=for-the-badge&logo=python" />`{=html}
  
`<img src="https://img.shields.io/badge/JAVASCRIPT-ES6+-yellow?style=for-the-badge&logo=javascript" />`{=html}
  
`<img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />`{=html}
:::

::: {align="center"}
`<img src="https://img.shields.io/badge/HTTPS-Local%20Secure-success?style=for-the-badge" />`{=html}
  
`<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />`{=html}
  
`<img src="https://img.shields.io/badge/STATUS-Active-success?style=for-the-badge" />`{=html}
:::

::: {align="center"}
`<img src="https://img.shields.io/badge/POETRY-Dependency%20Management-blueviolet?style=for-the-badge&logo=python" />`{=html}
:::

## Language

🇺🇸 English \| 🇧🇷 [Português](README_PT-Br.md)

------------------------------------------------------------------------

# 🚀 Overview

MultiPrint Web Agent is a local printing agent that exposes a **secure
HTTP API** for integration with external systems, abstracting printer
drivers, printer types, and operating system complexity.

It allows applications to send print jobs via HTTPS while the agent
handles validation, security, and dispatching to:

-   Laser printers
-   Thermal printers (Zebra / ZPL)

------------------------------------------------------------------------

# ✨ Key Features

-   🖨️ Laser and Thermal (ZPL) support
-   🔐 Session-based authentication
-   🚦 Per-route rate limiting
-   🧠 Automatic payload detection
-   📊 Agent state via API
-   🧪 Local UI for configuration
-   🧱 Modular architecture

------------------------------------------------------------------------

# 🚀 Quick Start (Development)

## 1️⃣ Set the API Key

### Windows (PowerShell)

``` powershell
setx MULTIPRINT_API_KEY "mp_dev_your_generated_key_here"
```

Restart terminal after setting.

### macOS / Linux

``` bash
export MULTIPRINT_API_KEY="mp_dev_your_generated_key_here"
```

------------------------------------------------------------------------

## 2️⃣ Generate SSL Certificate

``` bash
mkdir certs
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/agent.key -out certs/agent.crt -days 365 -subj "/CN=localhost"
```

------------------------------------------------------------------------

## 3️⃣ Install Dependencies

``` bash
poetry install
```

------------------------------------------------------------------------

## 4️⃣ Run the Agent

``` bash
poetry run python -m multiprint_web_agent.app
```

------------------------------------------------------------------------

# 🔌 API Endpoints

## POST /api/auth/handshake

Returns session token:

``` json
{
  "token": "SESSION_TOKEN",
  "expires_in": 1800
}
```

## POST /api/print

Headers:

    Authorization: Bearer <SESSION_TOKEN>
    Content-Type: application/json

Body example:

``` json
{
  "raw": "^XA^FO50,50^FDHello World^FS^XZ"
}
```

------------------------------------------------------------------------

# 📦 Print Payload

Required field:

-   `raw`

Optional:

-   `contentType`
-   `encoding`

Automatic detection supports:

-   ZPL
-   PDF
-   Images (PNG/JPEG)
-   Text fallback

------------------------------------------------------------------------

# 🔐 Security Model

-   API key via environment variable
-   Session tokens
-   Token expiration (TTL)
-   Rate limiting
-   HTTPS required

------------------------------------------------------------------------

# 🏗 Architecture

Organized by responsibility:

-   security
-   payload
-   printers
-   printing
-   observability
-   core

Backend: Flask (Blueprints)\
Frontend: JavaScript (ES Modules)\
Transport: HTTPS (self-signed in development)

------------------------------------------------------------------------

# ⚙️ Configuration

-   `certs/` → SSL certificate and key
-   `config/security.json` → session configuration (versioned)

------------------------------------------------------------------------

# 🛠 Development Setup (Poetry)

``` bash
poetry install
poetry run python -m multiprint_web_agent.app
```

Dependencies managed via `pyproject.toml`.

------------------------------------------------------------------------

# 📦 Project Status

Version: v1.0.0

-   Architecture consolidated
-   Production-ready for local environments

------------------------------------------------------------------------

# 🧭 Roadmap

✅ Phase 1 --- Setup\
✅ Phase 2 --- Payload Detection\
✅ Phase 3 --- Printer Configuration\
✅ Phase 4 --- Web UI\
✅ Phase 5 --- UX Refinement\
✅ Phase 6 --- New Features\
✅ Phase 7 --- Robustness & Security\
⬜ Phase 8 --- Production Packaging

------------------------------------------------------------------------

# 📝 License

MIT License\
Copyright © 2026 --- Pedro Godoy
