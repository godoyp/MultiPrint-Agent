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

> ⚠️ A porta padrão do agente é **9108**.  
> Caso essa porta já esteja em uso na sua máquina, é possível alterá-la no arquivo  
> `config/agent_config.json`, ajustando a propriedade `agent_port`.

---

## 🔐 Por que HTTPS é necessário

Navegadores modernos **bloqueiam requisições inseguras (HTTP)** ao acessar:
- APIs locais
- Serviços de impressão
- Recursos em nível de sistema

Executar o agente utilizando **HTTPS** evita:
- Problemas de CORS
- Erros de *mixed content*
- Bloqueios de segurança do navegador

> ⚠️ O certificado SSL utilizado é **autoassinado** e **gerado automaticamente durante o processo de instalação** do agente.

---

## 🌐 Aviso do navegador (comportamento esperado)

Como o certificado SSL utilizado é **autoassinado**, o navegador exibirá um **aviso de segurança no primeiro acesso**.  
**Esse comportamento é normal e esperado.**

### Passos:
1. Acesse `https://localhost:<PORT>/ui`
2. Escolha a opção **Avançado** / **Prosseguir mesmo assim**
3. Confirme a confiança no certificado

Após isso, o aviso não será exibido novamente para o mesmo navegador.

---

## 🚀 Inicialização do agente com HTTPS

O agente carrega automaticamente o certificado SSL durante a inicialização,  
não sendo necessária nenhuma configuração manual por parte do usuário.

---

## 🧠 Filosofia de Design

O MultiPrint Web Agent foi projetado para **simplificar integrações** e **isolar a complexidade da impressão** do lado do client.

Princípios fundamentais:

- O **client não precisa saber** o tipo de impressora utilizada
- O agente detecta automaticamente se a impressora é:
  - térmica (Zebra / ZPL)
  - ou genérica (laser)
- A lógica específica de hardware fica **centralizada no agente**, não espalhada nos sistemas clientes

Isso garante integrações que são:
- ✅ Simples  
- ✅ Estáveis  
- ✅ Independentes de modelo ou fabricante de impressora  

O campo `raw` atua como o **contrato da API** entre sistemas externos e o MultiPrint Web Agent, permitindo que o client envie dados sem precisar conhecer detalhes de renderização, drivers ou spool do sistema operacional.

Esse modelo reduz acoplamento, facilita manutenção e permite que o ambiente de impressão evolua sem impacto nas integrações existentes.

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

## 🧭 Roadmap

### ✅ Fase 1 — Configuração Inicial
Estrutura básica do agente, setup do projeto e bootstrap do servidor.

### ✅ Fase 2 — Payload Genérico
Suporte a diferentes tipos de payload (ZPL, PDF, imagens), com detecção automática.

### ✅ Fase 3 — Configuração de Impressoras
Seleção e persistência de impressoras laser e térmicas.

### ✅ Fase 4 — Interface Web
Criação da UI local para configuração e diagnóstico do agente.

### ✅ Fase 5 — Refinamento de UI & UX
Melhorias visuais, feedbacks, estados e experiência do usuário.

### ✅ Fase 6 — Novas Funcionalidades
Test print, logs, classificação de impressoras e recursos adicionais.

### ✅ Fase 7 — Robustez & Segurança
Session tokens, rate limit, validações, tratamento de falhas e hardening geral.

### ⬜ Fase 8 — Produção
Empacotamento final, documentação completa e preparação para uso em produção.

---

## 📝 Licença

MIT License

Copyright © 2026 — MultiPrint Web Agent
