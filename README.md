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

---

**MultiPrint Web Agent** é um agente local de impressão que expõe uma **API HTTP simples** para integração com sistemas externos, abstraindo a complexidade de drivers, tipos de impressoras e sistema operacional.

Ele permite que qualquer aplicação envie jobs de impressão via HTTP, enquanto o agente resolve segurança, validação e despacho para impressoras **laser** ou **térmicas (Zebra)**.

---

## ✨ Principais características

- 🖨️ Suporte a impressoras **Laser** e **Térmicas (ZPL / Zebra)**
- 🌐 API HTTP simples e previsível
- 🔐 Segurança com **session token**
- 🚦 Rate limit por rota
- 🧠 Detecção e validação de payload
- 📊 Estado do agente disponível via API
- 🧪 UI local para configuração e diagnóstico
- 🧱 Arquitetura modular e extensível

---

## 🏗️ Visão geral

```
External Client
      ↓
MultiPrint Web Agent
      ↓
System Printers (Laser / Thermal)
```

O client **nunca fala diretamente com a impressora**.  
Toda a lógica de validação, decisão e despacho acontece dentro do agente.

---

## 🔌 API – Endpoints principais

### 🔐 POST /auth/handshake

Cria uma sessão e retorna um **session token**.

```json
{
  "token": "SESSION_TOKEN",
  "expires_in": 1800
}
```

---

### 🖨️ POST /print

Envia um job de impressão.

**Headers**
```
Authorization: Bearer <SESSION_TOKEN>
Content-Type: application/json
```

**Body (exemplo ZPL)**
```json
{
  "raw": "^XA^FO50,50^FDHello World^FS^XZ"
}
```

---

### 📊 GET /state

Retorna o estado atual do agente.

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

## 🧪 UI local (Configuração)

O agente inclui uma **UI local** usada apenas para:

- Listar impressoras do sistema
- Classificar impressoras (laser / térmica)
- Selecionar impressora por função
- Executar test print
- Visualizar logs
- Ver estado do agente

> ⚠️ A UI **não faz parte da integração externa**  
> Ela existe apenas para setup e diagnóstico local.

---

## 🔐 Segurança

- Session token obrigatório para rotas protegidas
- Rate limit por rota
- Handshake restrito ao ambiente local
- Tokens renováveis automaticamente pelo client em caso de expiração

---

## 🧠 Arquitetura interna

- security – autenticação, sessão, rate limit
- payload – detecção e validação
- printers – detecção e status
- printing – renderização e despacho
- observability – logs e eventos
- core – configuração e estado do agente

---

## 🚀 Exemplo de integração (JavaScript)

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

async function printZpl(zpl) {
  let token = await getToken();

  let res = await fetch("https://localhost:9108/print", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ raw: zpl })
  });

  if (res.status === 401) {
    token = await getToken(true);
    res = await fetch("https://localhost:9108/print", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ raw: zpl })
    });
  }

  if (!res.ok) {
    throw new Error("Print failed");
  }
}
```

---

## 📦 Status do projeto

**Versão atual:** `v1.0.0`

✔️ Arquitetura consolidada  
✔️ Fluxos bem definidos  
✔️ Pronto para uso local em produção  

---

## 📝 Licença

MIT License

Copyright © 2026 — MultiPrint Web Agent
