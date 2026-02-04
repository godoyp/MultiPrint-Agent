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

## 📦 Payload de impressão

O endpoint `/print` aceita um payload flexível.  
O único campo **obrigatório** é `raw`.

Campos adicionais **não são obrigatórios**, mas **auxiliam o agente na identificação correta do tipo de payload**, tornando o processamento mais confiável.

### Campos suportados

| Campo          | Obrigatório | Descrição |
|---------------|-------------|-----------|
| `raw`         | ✅ Sim      | Conteúdo bruto a ser impresso |
| `contentType` | ❌ Não      | Tipo MIME do conteúdo (ex: `application/pdf`) |
| `encoding`    | ❌ Não      | Codificação do payload (ex: `base64`) |

---

### 🔍 Como o agente identifica o payload

O agente utiliza uma combinação de **inspeção de conteúdo** e **metadados auxiliares**:

- **ZPL**
  - Detectado automaticamente pela presença de comandos `^XA` e `^XZ`
  - Não requer `contentType` ou `encoding`

- **PDF**
  - Pode ser identificado por:
    - `contentType: application/pdf`
    - ou assinatura `%PDF` após decodificação base64

- **Imagens**
  - Identificadas por assinatura binária (PNG ou JPEG) após decodificação base64

- **Texto**
  - Utilizado como fallback quando nenhum padrão específico é detectado

Campos como `contentType` e `encoding` **não são obrigatórios**, mas ajudam o agente a identificar o tipo correto de payload de forma mais precisa, especialmente em cenários ambíguos.

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

  // Token expirado → renova e tenta novamente
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

// Exemplo ZPL (campos auxiliares não necessários)
printPayload({
  raw: "^XA^FO50,50^FDHello World^FS^XZ"
});

// Exemplo PDF (base64 + metadados auxiliares)
printPayload({
  raw: pdfBase64,
  encoding: "base64",
  contentType: "application/pdf"
});

// Exemplo imagem (PNG/JPEG em base64)
printPayload({
  raw: imageBase64,
  encoding: "base64",
  contentType: "image/png"
});
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

## 🏗️ Arquitetura

O MultiPrint Web Agent foi projetado com foco em **modularidade**, **clareza de responsabilidades** e **facilidade de evolução**.

### 🔧 Visão técnica

- Backend em **Flask**, organizado com **Blueprints**
- Motores de impressão modulares:
  - `print_zebra` (impressão térmica / ZPL)
  - `print_laser` (impressão genérica / SO)
- Carregamento centralizado de configurações
- Logs em tempo real via **SSE (Server-Sent Events)**
- UI Web local desenvolvida em **JavaScript ES6+ (ES Modules)**
- Servidor local executando com **HTTPS** e certificado autoassinado

### 🧠 Arquitetura interna (por responsabilidade)

O código é organizado por domínios bem definidos:

- **security**  
  Autenticação, sessão, rate limit e controles de acesso

- **payload**  
  Detecção, normalização e validação de dados de impressão

- **printers**  
  Detecção de impressoras, verificação de status e classificação

- **printing**  
  Renderização e despacho de jobs para o sistema operacional

- **observability**  
  Logs, eventos e mecanismos de diagnóstico

- **core**  
  Configuração central e estado runtime do agente

Essa separação garante baixo acoplamento, facilita testes e permite evolução do sistema sem impactos nas integrações existentes.

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
