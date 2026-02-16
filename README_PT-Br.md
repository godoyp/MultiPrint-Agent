<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/multiprint_web_agent/static/images/logo-white.png">
    <source media="(prefers-color-scheme: light)" srcset="/multiprint_web_agent/static/images/logo.png">
    <img src="/multiprint_web_agent/static/images/logo-white.png" width="150">
  </picture>
</p>

<h1 align="center">MultiPrint Web Agent</h1>


  <div align="center">
    <img src="https://img.shields.io/badge/PYTHON-3.11.9-blue?style=for-the-badge&logo=python" />
    &nbsp;&nbsp;
    <img src="https://img.shields.io/badge/JAVASCRIPT-ES6+-yellow?style=for-the-badge&logo=javascript" />
    &nbsp;&nbsp;
    <img src="https://img.shields.io/badge/FLASK-Backend-black?style=for-the-badge&logo=flask" />
  </div>
  <div align="center">
    <img src="https://img.shields.io/badge/HTTPS-Local%20Secure-success?style=for-the-badge" />
    &nbsp;&nbsp;
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />
    &nbsp;&nbsp;
    <img src="https://img.shields.io/badge/STATUS-Active-success?style=for-the-badge" />
  </div>
  <div align="center">
    <img src="https://img.shields.io/badge/POETRY-Dependency%20Management-blueviolet?style=for-the-badge&logo=python" />
  </div>

## Idioma:
🇺🇸 English \| 🇧🇷 [Português](README_PT-Br.md)

------------------------------------------------------------------------

**MultiPrint Web Agent** é um agente de impressão local que expõe uma
**API HTTP simples** para integração com sistemas externos, abstraindo a
complexidade de drivers de impressora, tipos de impressora e do sistema
operacional.

Ele permite que qualquer aplicação envie trabalhos de impressão via
HTTP, enquanto o agente gerencia segurança, validação e o envio para
impressoras **laser** ou **térmicas (Zebra)**.

Este projeto é ideal para sistemas que precisam **imprimir localmente**
sem lidar diretamente com:

-   drivers de impressora
-   spoolers do sistema operacional
-   diferenças entre impressoras laser e térmicas

------------------------------------------------------------------------

## 📑 Índice

-   [✨ Principais Funcionalidades](#-principais-funcionalidades)
-   [🏗️ Visão Geral](#️-visão-geral)
-   [🔐 Por Que HTTPS É Necessário](#-por-que-https-é-necessário)
-   [🌐 Aviso do Navegador (Esperado)](#-browser-warning-expected)
-   [🧠 Filosofia de Design](#-design-philosophy)
-   [❌ O Que Este Projeto Não É](#-what-this-project-is-not)
-   [📦 Payload de Impressão](#-print-payload)
-   [🔌 API -- Principais Endpoints](#-api--main-endpoints)
-   [🚀 Exemplo de Integração (JavaScript)](#-integration-example-javascript)
-   [🧪 Interface Local (Configuração)](#-local-ui-configuration)
-   [🏗️ Arquitetura](#️-architecture)
-   [🔐 Segurança](#-security)
-   [🧪 Setup de Desenvolvimento (Execução Manual)](#-development-setup-manual-execution)
-   [🛠️ Poetry](#️-poetry)
-   [📦 Status do Projeto](#-project-status)
-   [📝 Licença](#-license)

------------------------------------------------------------------------

## ✨ Principais Funcionalidades

-   🖨️ Suporte para impressoras **Laser** e **Térmicas (ZPL / Zebra)**
-   🌐 API HTTP simples e previsível
-   🔐 Segurança com **tokens de sessão**
-   🚦 Limitação de requisições por rota (rate limiting)
-   🧠 Detecção e validação automática de payload
-   📊 Estado do agente disponível via API
-   🧪 Interface local para configuração e diagnósticos
-   🧱 Arquitetura modular e extensível

------------------------------------------------------------------------

## 🏗️ Visão Geral

    External Client
          ↓
    MultiPrint Web Agent
          ↓
    System Printers (Laser / Thermal)

O cliente **nunca se comunica diretamente com a impressora**.\
Toda validação, tomada de decisão e lógica de envio acontece dentro do
agente.

> ⚠️ A porta padrão do agente é **9108**.\
> Se esta porta já estiver em uso na sua máquina, você pode alterá-la
> em\
> `config/agent.json` ajustando a propriedade `agent_port`.

------------------------------------------------------------------------

## 🔐 Por Que HTTPS É Necessário

Navegadores modernos **bloqueiam requisições inseguras (HTTP)** ao
acessar:

-   APIs locais
-   Serviços de impressão
-   Recursos em nível de sistema

Executar o agente utilizando **HTTPS** evita:

-   Problemas de CORS
-   Erros de conteúdo misto
-   Bloqueios de segurança do navegador

> ⚠️ O certificado SSL utilizado é **autoassinado** e **gerado
> automaticamente durante o processo de instalação do agente**.

------------------------------------------------------------------------

## 🌐 Aviso do Navegador (Esperado)

Como o certificado SSL é **autoassinado**, o navegador exibirá um
**aviso de segurança no primeiro acesso**.\
**Esse comportamento é normal e esperado.**

### Passos:

1.  Abra `https://localhost:<PORT>/ui`
2.  Escolha **Avançado** / **Continuar mesmo assim**
3.  Confirme a confiança no certificado

Após isso, o aviso não aparecerá novamente para o mesmo navegador.

------------------------------------------------------------------------

## 🧠 Filosofia de Design

O MultiPrint Web Agent foi projetado para **simplificar integrações** e
**isolar a complexidade de impressão** do lado do cliente.

Princípios principais:

-   O **cliente não precisa saber** o tipo de impressora
-   O agente detecta automaticamente se a impressora é:
    -   térmica (Zebra / ZPL)
    -   ou genérica (laser)
-   A lógica específica de hardware é **centralizada no agente**, não
    espalhada pelos sistemas clientes

Isso garante integrações que são:

-   ✅ Simples\
-   ✅ Estáveis\
-   ✅ Independentes de impressora

O campo `raw` atua como o **contrato da API** entre sistemas externos e
o MultiPrint Web Agent, permitindo que clientes enviem dados sem
precisar entender detalhes de renderização, drivers ou spoolers do
sistema operacional.

Esse modelo reduz acoplamento, simplifica manutenção e permite que o
ambiente de impressão evolua sem impactar integrações existentes.

------------------------------------------------------------------------

## ❌ O Que Este Projeto Não É

Para definir claramente o escopo, o MultiPrint Web Agent:

-   ❌ Não é um serviço de impressão em nuvem
-   ❌ Não expõe impressoras diretamente na rede
-   ❌ Não substitui drivers do sistema operacional
-   ❌ Não exige que clientes entendam detalhes de hardware

O objetivo do projeto é **centralizar e abstrair a complexidade da
impressão local**, mantendo integrações simples e estáveis.

------------------------------------------------------------------------

## 📦 Payload de Impressão

O endpoint `/api/print` aceita um payload flexível.\
O único campo **obrigatório** é `raw`.

Campos adicionais são **opcionais**, mas **ajudam o agente a identificar
o tipo de payload com maior precisão**, tornando o processamento mais
confiável.

### Campos suportados

  ------------------------------------------------------------------------
  Campo                        Obrigatório            Descrição
  ---------------------------- ---------------------- --------------------
  `raw`                        ✅ Sim                 Conteúdo bruto a ser
                                                      impresso

  `contentType`                ❌ Não                 Tipo MIME do
                                                      conteúdo (ex:
                                                      `application/pdf`)

  `encoding`                   ❌ Não                 Codificação do
                                                      payload (ex:
                                                      `base64`)
  ------------------------------------------------------------------------

### 🔍 Como o agente detecta o payload

O agente utiliza uma combinação de **inspeção de conteúdo** e
**metadados auxiliares**:

-   **ZPL**
    -   Detectado automaticamente pela presença dos comandos `^XA` e
        `^XZ`
    -   Não requer `contentType` ou `encoding`
-   **PDF**
    -   Identificado por:
        -   `contentType: application/pdf`
        -   ou assinatura `%PDF` após decodificação base64
-   **Imagens**
    -   Identificadas por assinaturas binárias (PNG ou JPEG) após
        decodificação base64
-   **Texto**
    -   Utilizado como fallback quando nenhum padrão específico é
        detectado

Campos como `contentType` e `encoding` **não são obrigatórios**, mas
ajudam o agente a tomar decisões mais precisas em cenários ambíguos.

------------------------------------------------------------------------

## 🔌 API -- Principais Endpoints

### 🔐 POST /api/auth/handshake

Cria uma sessão e retorna um **token de sessão**.

``` json
{
  "token": "SESSION_TOKEN",
  "expires_in": 1800
}
```

### 🖨️ POST /api/print

Envia um trabalho de impressão.

**Headers**

    Authorization: Bearer <SESSION_TOKEN>
    Content-Type: application/json

**Body (exemplo ZPL)**

``` json
{
  "raw": "^XA^FO50,50^FDHello World^FS^XZ"
}
```

------------------------------------------------------------------------

## 🚀 Exemplo de Integração (JavaScript)

(O código permanece exatamente igual ao original.)

``` js
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
```

------------------------------------------------------------------------

## 🏗️ Arquitetura

O MultiPrint Web Agent foi projetado com foco em **modularidade**,
**responsabilidades claras** e **facilidade de evolução**.

> ℹ️ Atualmente, o agente é focado em ambientes **Windows**, devido à
> integração direta com o subsistema de impressão do sistema
> operacional.

### 🔧 Visão técnica

-   Backend **Flask** organizado com **Blueprints**
-   Módulos de impressão:
    -   `print_zebra` (térmica / ZPL)
    -   `print_laser` (genérica / sistema operacional)
-   Carregamento centralizado de configurações
-   Logs em tempo real via **SSE (Server-Sent Events)**
-   UI local construída com **JavaScript ES6+ (ES Modules)**
-   Servidor local executando com **HTTPS** e certificado autoassinado

### 🧠 Arquitetura interna (por responsabilidade)

O código é organizado em domínios bem definidos:

-   **security**\
    Autenticação, sessões, rate limiting e controle de acesso

-   **payload**\
    Detecção, normalização e validação de dados de impressão

-   **printers**\
    Detecção, status e classificação de impressoras

-   **printing**\
    Renderização e envio de trabalhos de impressão para o sistema

-   **observability**\
    Logs, eventos e diagnósticos

-   **core**\
    Configuração central e estado de execução do agente

Essa separação garante baixo acoplamento, facilidade de testes e
evolução futura sem quebrar integrações existentes.

------------------------------------------------------------------------

## 🔐 Segurança

-   Tokens de sessão obrigatórios para rotas protegidas
-   Rate limiting por rota
-   Handshake restrito ao ambiente local
-   Renovação automática de token pelo cliente quando expirado

As seções abaixo descrevem como a segurança é configurada e aplicada.

### Configuração de Segurança

O MultiPrint Web Agent separa **segredos** de **configurações
comportamentais de segurança**.

Isso garante uma configuração segura mantendo o sistema flexível entre
diferentes ambientes.

### Variável de Ambiente

A chave de API usada para autenticar clientes externos **é fornecida via
variável de ambiente e gerada durante o processo de instalação**.

Esse valor é considerado sensível e **não deve ser armazenado em
arquivos de configuração ou versionado**.

### Variável obrigatória

-   `MULTIPRINT_API_KEY`\
    Chave de API usada por sistemas externos para autenticar requisições
    de impressão.

Se essa variável não estiver definida, o agente não iniciará.

### Configuração de TTL de Sessão

O tempo de expiração da sessão é configurável via arquivo
`security.json`.

``` json
{
  "session_ttl": 1800
}
```

-   O valor é expresso em **segundos**
-   O arquivo não contém segredos
-   É seguro mantê-lo versionado
-   Se estiver ausente, um valor padrão seguro será utilizado

### Como funciona a expiração da sessão

-   O TTL é carregado a partir de `security.json`
-   O valor é aplicado durante `/auth/handshake`
-   Cada token recebe seu próprio timestamp de expiração
-   Tokens expirados são automaticamente invalidados

### Justificativa de Design

-   **Segredos** (chaves de API) são carregados via variáveis de
    ambiente
-   **Comportamento de segurança** (como tempo de sessão) é carregado
    via arquivos de configuração
-   A lógica de sessão permanece desacoplada da política de segurança

Essa separação evita exposição acidental de segredos e mantém o agente
flexível entre ambientes.

### Certificado

Por razões de segurança, alguns arquivos **não são versionados no
repositório**:

-   `certs/`\
    Contém o certificado SSL (`.crt`) e a chave privada (`.key`) usados
    pelo agente.

**Esses arquivos são gerados durante o processo de instalação do
agente.**

------------------------------------------------------------------------

## 🧪 Setup de Desenvolvimento (Execução Manual)

Ao executar o agente diretamente via Python (modo de desenvolvimento),
você deve garantir manualmente que:

-   o diretório `certs/` exista
-   o certificado SSL e a chave privada estejam presentes
-   a variável de ambiente `MULTIPRINT_API_KEY` esteja definida

### 🔐 Gerando um Certificado SSL para Localhost (Apenas Desenvolvimento)

Para ambientes de desenvolvimento, é necessário gerar manualmente um
**certificado autoassinado** para `localhost`.

### Passo 1 --- Instalar o OpenSSL

Certifique-se de que o OpenSSL está instalado e disponível no PATH do
sistema.

Para verificar:

``` bash
openssl version
```

Se o comando não for reconhecido, instale o OpenSSL e reinicie o
terminal.

### Passo 2 --- Criar o diretório `certs`

Dentro da raiz do projeto:

``` bash
mkdir certs
```

### Passo 3 --- Gerar o certificado e a chave

Execute o seguinte comando na raiz do projeto:

``` bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/agent.key -out certs/agent.crt -days 365 -subj "/CN=localhost"
```

Isso irá gerar:

-   `certs/agent.key`
-   `certs/agent.crt`

O certificado será válido por **365 dias**.

### Definir a API Key

#### PowerShell

``` powershell
setx MULTIPRINT_API_KEY "mp_dev_your_generated_key_here"
```

------------------------------------------------------------------------

## 🛠️ Poetry

O MultiPrint Web Agent utiliza **Poetry** para gerenciamento de
dependências e empacotamento.

### Requisitos

-   Python 3.11+
-   Poetry instalado

### Instalar o Poetry

Se não estiver instalado:

``` bash
pip install poetry
```

Ou siga as instruções oficiais: https://python-poetry.org/docs/

### Instalar dependências

Na raiz do projeto:

``` bash
poetry install
```

### Executar o agente (Modo Desenvolvimento)

``` bash
poetry run python -m multiprint_web_agent.app
```

O agente iniciará utilizando HTTPS na porta configurada.

### Adicionar novas dependências

Dependência de runtime:

``` bash
poetry add <nome-do-pacote>
```

Dependência apenas de desenvolvimento:

``` bash
poetry add --group dev <nome-do-pacote>
```

### Arquivo de dependências

Todas as dependências são definidas em:

`pyproject.toml`

Não existe arquivo `requirements.txt` neste projeto.

------------------------------------------------------------------------

## 📦 Status do Projeto

**Versão atual:** `v1.0.0`

✔️ Arquitetura consolidada\
✔️ Fluxos bem definidos\
✔️ Pronto para uso local em produção

------------------------------------------------------------------------

## 📝 Licença

MIT License

Copyright © 2026 --- Pedro Godoy - MultiPrint Web Agent
