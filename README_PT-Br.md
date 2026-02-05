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

**MultiPrint Web Agent** é um agente local de impressão que expõe uma **API HTTP simples** para integração com sistemas externos, abstraindo a complexidade de drivers de impressora, tipos de impressora e do sistema operacional.

Ele permite que qualquer aplicação envie jobs de impressão via HTTP, enquanto o agente lida com segurança, validação e despacho para impressoras **laser** ou **térmicas (Zebra)**.

Este projeto é ideal para sistemas que precisam **imprimir localmente** sem lidar diretamente com:
- drivers de impressora
- spoolers do sistema operacional
- diferenças entre impressoras laser e térmicas

---

## ✨ Principais Características

- 🖨️ Suporte a impressoras **Laser** e **Térmicas (ZPL / Zebra)**
- 🌐 API HTTP simples e previsível
- 🔐 Segurança com **tokens de sessão**
- 🚦 Rate limit por rota
- 🧠 Detecção e validação de payload
- 📊 Estado do agente disponível via API
- 🧪 UI local para configuração e diagnóstico
- 🧱 Arquitetura modular e extensível

---

## 🏗️ Visão Geral

```
Cliente Externo
      ↓
MultiPrint Web Agent
      ↓
Impressoras do Sistema (Laser / Térmica)
```

O cliente **nunca se comunica diretamente com a impressora**.  
Toda a lógica de validação, tomada de decisão e despacho acontece dentro do agente.

> ⚠️ A porta padrão do agente é **9108**.  
> Se esta porta já estiver em uso na sua máquina, você pode alterá-la em  
> `config/agent.json`, ajustando a propriedade `agent_port`.

---

## 🔐 Por que HTTPS é Necessário

Navegadores modernos **bloqueiam requisições inseguras (HTTP)** ao acessar:
- APIs locais
- Serviços de impressão
- Recursos em nível de sistema

Executar o agente usando **HTTPS** evita:
- Problemas de CORS
- Erros de *mixed content*
- Bloqueios de segurança do navegador

> ⚠️ O certificado SSL utilizado é **autoassinado** e **gerado automaticamente durante o processo de instalação do agente**.

---

## 🌐 Aviso do Navegador (Esperado)

Como o certificado SSL é **autoassinado**, o navegador exibirá um **aviso de segurança no primeiro acesso**.  
**Este comportamento é normal e esperado.**

### Passos:
1. Acesse `https://localhost:<PORT>/ui`
2. Escolha **Avançado** / **Prosseguir mesmo assim**
3. Confirme a confiança no certificado

Após isso, o aviso não aparecerá novamente para o mesmo navegador.

---

## 🧠 Filosofia de Design

O MultiPrint Web Agent foi projetado para **simplificar integrações** e **isolar a complexidade da impressão** do lado do cliente.

Princípios centrais:

- O **cliente não precisa saber** o tipo de impressora
- O agente detecta automaticamente se a impressora é:
  - térmica (Zebra / ZPL)
  - ou genérica (laser)
- A lógica específica de hardware é **centralizada no agente**, e não espalhada pelos sistemas clientes

Isso garante integrações que são:
- ✅ Simples  
- ✅ Estáveis  
- ✅ Independentes de impressora  

O campo `raw` atua como o **contrato da API** entre sistemas externos e o MultiPrint Web Agent, permitindo que clientes enviem dados sem precisar entender detalhes de renderização, drivers ou spool do sistema operacional.

Este modelo reduz acoplamento, simplifica a manutenção e permite que o ambiente de impressão evolua sem impactar integrações existentes.

## ❌ O que Este Projeto Não É

Para definir claramente o escopo, o MultiPrint Web Agent:

- ❌ Não é um serviço de impressão em nuvem
- ❌ Não expõe impressoras diretamente para a rede
- ❌ Não substitui drivers do sistema operacional
- ❌ Não exige que clientes entendam detalhes de hardware

O objetivo do projeto é **centralizar e abstrair a complexidade da impressão local**, mantendo integrações simples e estáveis.

---

## 📦 Payload de Impressão

O endpoint `/print` aceita um payload flexível.  
O único campo **obrigatório** é `raw`.

Campos adicionais são **opcionais**, mas **ajudam o agente a identificar o tipo de payload com mais precisão**, tornando o processamento mais confiável.

### Campos suportados

| Campo         | Obrigatório | Descrição |
|---------------|-------------|-----------|
| `raw`         | ✅ Sim      | Conteúdo bruto a ser impresso |
| `contentType` | ❌ Não      | Tipo MIME do conteúdo (ex: `application/pdf`) |
| `encoding`    | ❌ Não      | Codificação do payload (ex: `base64`) |

---

### 🔍 Como o agente detecta o payload

O agente utiliza uma combinação de **inspeção de conteúdo** e **metadados auxiliares**:

- **ZPL**
  - Detectado automaticamente pela presença dos comandos `^XA` e `^XZ`
  - Não requer `contentType` ou `encoding`

- **PDF**
  - Identificado por:
    - `contentType: application/pdf`
    - ou assinatura `%PDF` após decodificação base64

- **Imagens**
  - Identificadas por assinaturas binárias (PNG ou JPEG) após decodificação base64

- **Texto**
  - Utilizado como fallback quando nenhum padrão específico é detectado

Campos como `contentType` e `encoding` **não são obrigatórios**, mas ajudam o agente a tomar decisões mais precisas em cenários ambíguos.

---

## 🔌 API – Principais Endpoints

### 🔐 POST /auth/handshake

Cria uma sessão e retorna um **token de sessão**.

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

## 🚀 Exemplo de Integração (JavaScript)

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

## 🧪 UI Local (Configuração)

O agente inclui uma **UI local** utilizada apenas para:

- Listar impressoras do sistema
- Classificar impressoras (laser / térmica)
- Selecionar impressoras por função
- Executar impressões de teste
- Visualizar logs
- Verificar o estado do agente

> ⚠️ A UI **não faz parte da integração externa**  
> Ela existe apenas para configuração e diagnóstico local.

---

## 🔐 Segurança

- Tokens de sessão obrigatórios para rotas protegidas
- Rate limit por rota
- Handshake restrito ao ambiente local
- Tokens renováveis automaticamente pelo cliente quando expirados

As seções abaixo descrevem como a segurança é configurada e aplicada.

## 🔐 Configuração de Segurança

O MultiPrint Web Agent separa **segredos** de **configurações comportamentais de segurança**.

Isso garante uma configuração segura mantendo o sistema fácil de adaptar a diferentes ambientes.

### Variável de Ambiente (Obrigatória)

A API key usada para autenticar clientes externos **deve ser fornecida via variável de ambiente**.

Este valor é sensível e **não deve ser armazenado em arquivos de configuração ou versionamento**.

#### Variável obrigatória

- `MULTIPRINT_API_KEY`  
  Chave de API usada por sistemas externos para autenticar requisições de impressão.

Se esta variável não estiver definida, o agente **não iniciará**.

### Configuração de TTL da Sessão

O tempo de expiração da sessão é configurável via arquivo `security.json`.

Esta configuração define por quanto tempo um token de sessão permanece válido após ser emitido.

```json
{
  "session_ttl": 1800 // 30 minutos
}
```

- O valor é expresso em **segundos**
- Este arquivo contém **configuração não sensível**
- É seguro mantê-lo sob versionamento
- Se o arquivo ou valor estiver ausente, um valor padrão seguro é utilizado

### Como Funciona a Expiração de Sessão

- O TTL da sessão é carregado a partir de `security.json`
- O valor é aplicado durante `/auth/handshake`
- Cada token emitido recebe seu próprio timestamp de expiração
- Tokens expirados são automaticamente invalidados

Este design mantém a política de sessão explícita, configurável e isolada da lógica de bootstrap de segurança.

### Racional de Design

- **Segredos** (API keys) são carregados via variáveis de ambiente
- **Comportamento de segurança** (como tempo de vida da sessão) é carregado via arquivos de configuração
- **Lógica de sessão** permanece stateless e agnóstica à política

Essa separação evita exposição acidental de segredos e mantém o agente flexível entre ambientes.

---

## 🏗️ Arquitetura

O MultiPrint Web Agent foi projetado com foco em **modularidade**, **clareza de responsabilidades** e **facilidade de evolução**.

> ℹ️ Atualmente, o agente é focado em ambientes **Windows** devido à integração direta com o subsistema de impressão do sistema operacional.

### 🔧 Visão Técnica

- Backend **Flask** organizado com **Blueprints**
- Motores de impressão modulares:
  - `print_zebra` (impressão térmica / ZPL)
  - `print_laser` (impressão genérica / SO)
- Carregamento centralizado de configurações
- Logs em tempo real via **SSE (Server-Sent Events)**
- UI Web local construída com **JavaScript ES6+ (ES Modules)**
- Servidor local executando com **HTTPS** e certificado autoassinado

### 🧠 Arquitetura Interna (por responsabilidade)

O código é organizado em domínios bem definidos:

- **security**  
  Autenticação, sessões, rate limit e controle de acesso

- **payload**  
  Detecção, normalização e validação de dados de impressão

- **printers**  
  Detecção de impressoras, verificação de status e classificação

- **printing**  
  Renderização e despacho de jobs de impressão para o SO

- **observability**  
  Logs, eventos e diagnósticos

- **core**  
  Configuração central e estado de execução do agente

Esta separação garante baixo acoplamento, testes mais fáceis e evolução futura sem quebrar integrações existentes.

---

## ⚙️ Arquivos de Configuração e Certificados

Por razões de segurança, alguns arquivos **não são versionados no repositório**:

- `certs/`  
  Contém o certificado SSL e a chave privada usados pelo agente.

- `config/security.json`  
  Contém configurações sensíveis relacionadas à segurança do agente.

Esses arquivos são **gerados automaticamente durante o processo de instalação do agente**.

### Execução manual (ambiente de desenvolvimento)

Se o agente for executado diretamente via Python, você deve garantir que:

- o diretório `certs/` exista
- o arquivo `config/security.json` esteja presente

O repositório inclui **arquivos de configuração de exemplo** que podem ser usados como ponto de partida:

- `config/security.example.json`

Esses arquivos devem ser copiados e ajustados localmente antes de executar o agente.

---

## 📦 Status do Projeto

**Versão atual:** `v1.0.0`

✔️ Arquitetura consolidada  
✔️ Fluxos bem definidos  
✔️ Pronto para uso local em produção  

---

## 🧭 Roadmap

### ✅ Fase 1 — Configuração Inicial
Estrutura base do agente, setup do projeto e bootstrap do servidor.

### ✅ Fase 2 — Payload Genérico
Suporte a múltiplos tipos de payload (ZPL, PDF, imagens) com detecção automática.

### ✅ Fase 3 — Configuração de Impressoras
Seleção e persistência de impressoras laser e térmicas.

### ✅ Fase 4 — UI Web
Criação da UI local para configuração e diagnóstico.

### ✅ Fase 5 — Refinamento de UI & UX
Melhorias visuais, feedbacks, estados e experiência do usuário.

### ✅ Fase 6 — Novas Funcionalidades
Impressão de teste, logs, classificação de impressoras e recursos adicionais.

### ✅ Fase 7 — Robustez & Segurança
Tokens de sessão, rate limit, validação, tratamento de falhas e hardening.

### ⬜ Fase 8 — Produção
Empacotamento final, documentação completa e prontidão para produção.

---

## 📝 Licença

Licença MIT

Copyright © 2026 — MultiPrint Web Agent
