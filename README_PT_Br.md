
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

**MultiPrint Web Agent** é um agente local de impressão que expõe uma **API HTTP simples** para integração com sistemas externos, abstraindo a complexidade de drivers de impressora, tipos de impressoras e do sistema operacional.

Ele permite que qualquer aplicação envie jobs de impressão via HTTP, enquanto o agente cuida da segurança, validação e despacho para impressoras **laser** ou **térmicas (Zebra)**.

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
Toda a lógica de validação, decisão e despacho acontece dentro do agente.

> ⚠️ A porta padrão do agente é **9108**.  
> Caso essa porta já esteja em uso na sua máquina, você pode alterá-la em  
> `config/agent.json`, ajustando a propriedade `agent_port`.

---

## 🔐 Por que HTTPS é Necessário

Navegadores modernos **bloqueiam requisições inseguras (HTTP)** ao acessar:
- APIs locais
- Serviços de impressão
- Recursos em nível de sistema

Executar o agente utilizando **HTTPS** evita:
- Problemas de CORS
- Erros de *mixed content*
- Bloqueios de segurança do navegador

> ⚠️ O certificado SSL utilizado é **autoassinado** e **gerado automaticamente durante o processo de instalação do agente**.

---

## 🌐 Aviso do Navegador (Esperado)

Como o certificado SSL é **autoassinado**, o navegador exibirá um **aviso de segurança no primeiro acesso**.  
**Esse comportamento é normal e esperado.**

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
- A lógica específica de hardware fica **centralizada no agente**, e não espalhada pelos sistemas clientes

Isso garante integrações:
- ✅ Simples  
- ✅ Estáveis  
- ✅ Independentes de impressora  

O campo `raw` atua como o **contrato da API** entre sistemas externos e o MultiPrint Web Agent, permitindo que clientes enviem dados sem precisar entender detalhes de renderização, drivers ou spool do sistema operacional.

Esse modelo reduz acoplamento, simplifica manutenção e permite que o ambiente de impressão evolua sem impactar integrações existentes.

## ❌ O que Este Projeto Não É

Para deixar o escopo claro, o MultiPrint Web Agent:

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
|--------------|-------------|----------|
| `raw`        | ✅ Sim      | Conteúdo bruto a ser impresso |
| `contentType`| ❌ Não      | Tipo MIME do conteúdo (ex: `application/pdf`) |
| `encoding`   | ❌ Não      | Codificação do payload (ex: `base64`) |

---

## 📝 Licença

MIT License

Copyright © 2026 — MultiPrint Web Agent
