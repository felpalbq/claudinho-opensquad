# Claudinho-OpenSquad

Memoria persistente e versionada para sessoes do Claude Code no projeto **OpenSquad**.

## O que e

O **Claudinho-OpenSquad** e o arquiteto-engenheiro de sistema do framework [OpenSquad](https://github.com/renatoasse/opensquad). Ele garante que cada sessao do Claude Code nunca comece do zero, carregando apenas o contexto relevante sob demanda.

> **Cada token carregado sem proposito e desperdicio.** O sistema deve ser um indice inteligente, nao um deposito.

## Filosofia central

- **Minimo que entrega valor** — nao caprichar antes da hora
- **Validar antes de avancar** — cada fase testada antes de avancar
- **Padroes inegociaveis sao fixos** — nao negociar, nao ver se funciona sem

## Arquitetura de Tiers

| Tier | Conteudo | Carregamento |
|---|---|---|
| **Tier 0** | `claudinho_state.json` + `meta/` | Sempre |
| **Tier 1** | `patterns/` | Sob demanda |
| **Tier 2** | `decisions/` + `projects/` | Sob demanda |
| **Tier 3** | `snapshots/` | Somente quando necessario |

## Estrutura de diretorios

```
brain/
├── claudinho_state.json      # Estado central — objetivo, foco, bloqueios
├── decisions/              # Decisoes estruturais com alternativas e rationale
│   └── index.json
├── patterns/               # Padroes validados e anti-padroes
│   └── patterns.json
├── projects/               # Contexto por projeto
│   └── index.json
├── snapshots/              # Snapshots de estados complexos
│   └── index.json
└── meta/                   # Metadados do sistema
    ├── index.json
    ├── schema.json
    ├── evolution.json
    ├── memory_policy.json
    ├── session_protocol.json
    └── operational_identity.json
```

## CLI

```bash
python brain.py start     # Inicializa sessao (git pull + validar + carrega Tier 0)
python brain.py load <t>  # Carrega contexto seletivo (decisions, patterns, project, decision:ID)
python brain.py save      # Valida e persiste (git add + commit + push)
python brain.py status    # Consulta estado atual
```

## Formato

- **JSON** em todos os arquivos
- **Git versionado**: todo `save` faz commit automatico
- **Loading seletivo**: nunca carrega tudo de uma vez

## Contexto do projeto

Este Claudinho e dedicado exclusivamente ao **OpenSquad**, framework multi-agente de orquestracao para producao de conteudo social.

**Stack:**
- Claude Code CLI + Ollama (kimi-k2.6 / glm-5.1)
- MCP servers: Playwright, Apify, Tavily, Composio
- Node.js 20+

**Nao confundir com:**
- Claudinho original (projeto Hermes/OpenClaw) — memoria separada, dominio separado
