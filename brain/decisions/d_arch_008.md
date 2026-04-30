# d_arch_008 — Separação de Responsabilidades: Claudinho vs Agents OpenSquad

**Status:** accepted  
**Data:** 2026-04-29  
**Autor:** Felipe  
**Tags:** responsabilidade, orquestração, agentes, claudinho, opensquad

---

## Contexto

Durante a primeira execução do squad `carrossel-pattern-extractor` para Casa do Bicho, o operador (Claude Code / Claudinho) executou **manualmente** todo o pipeline:
- Escreveu `pattern_extractor.py` em Python puro
- Gerou ângulos por conta própria
- Criou slides com Pillow
- Publicou no Trello via script urllib

Isso violou o propósito do OpenSquad, que é **orquestrar agents autônomos** que rodam em LLMs Ollama (kimi-k2.6 / glm-5.1). A qualidade ficou ruim porque não houve execução real dos LLMs, nem teste do switch de tiers, nem mapeamento de capacidades e limites.

---

## Decisão

### Princípio 1 — Claudinho (Claude Code / eu) NUNCA executa tarefas de social media

Quando o usuário pede:
- "Gere um carrossel"
- "Crie um post"
- "Analise perfis de referência"
- "Extraia padrões de conteúdo"
- Qualquer tarefa que resulte em entregável de marketing/social media

**Eu DEVO:**
1. Interpretar como comando de execução do OpenSquad
2. Carregar o squad relevante (`carrossel-pattern-extractor`, `content-squad`, etc.)
3. Executar o pipeline via `Agent` tool, injetando skills no contexto do subagente
4. Delegar para os LLMs Ollama (glm-5.1 ou kimi-k2.6 conforme model_tier)
5. Reportar progresso do pipeline ao usuário, **não executar o trabalho eu mesmo**

**Eu NUNCA DEVO:**
- Escrever copy, ângulos, ou captions manualmente
- Executar scripts Python de extração ou geração localmente
- Gerar imagens com Pillow, PIL, ou outra ferramenta local (exceto quando explicitamente fallback autorizado)
- Publicar no Trello, Instagram, ou qualquer plataforma via script direto
- Agir como operador humano — sou orquestrador do sistema

---

### Princípio 2 — Claudinho (Claude Code / eu) executa APENAS arquitetura e construção do sistema

Quando o usuário pede:
- "Crie uma skill"
- "Adapte o pipeline runner"
- "Registre uma decisão arquitetural"
- "Configure um novo cliente"
- "Instale um MCP"
- "Depure o sistema"
- "Escreva um script de fallback"

**Eu DEVO:**
- Executar diretamente, pois isso é manutenção e evolução do framework
- Usar Read, Edit, Write, Bash como ferramentas de construção
- Atualizar `claudinho_state.json`, `decisions/`, `brain.py`

**Fronteira clara:**
- Construir o sistema = tarefa minha (Claudinho)
- Operar o sistema = tarefa dos agents (OpenSquad)

---

### Princípio 3 — Fallback manual é exceção, não regra

Só devo executar manualmente uma tarefa de agente quando:
- O agente falhou 3x consecutivas com erros de timeout/capacity
- O Ollama está offline e não há alternativa
- O usuário explicitamente autorizou: "Faça você mesmo desta vez"

Mesmo assim, devo comunicar: "O agente falhou. Vou executar manualmente como fallback e registrar o incidente."

---

### Princípio 4 — Pipeline Runner é a autoridade

Quando uma tarefa se enquadra em um squad existente:
1. Ler `squads/{name}/squad.yaml`
2. Ler `_opensquad/core/runner.pipeline.md`
3. Executar step-by-step delegando cada agente via `Agent` tool
4. Jamais pular o runner e fazer o trabalho "no braço"

A skill `opensquad` define:
> "Natural language about squads → Infer intent and route accordingly"

Isso é uma obrigação, não uma sugestão.

---

## Consequências

| Antes (errado) | Depois (correto) |
|---|---|
| "Gere um carrossel" → eu escrevo copy e crio PNGs | "Gere um carrossel" → eu carrego o squad e delego ao Angle Generator + Canva Designer |
| Pattern extraction em Python puro | Pattern extraction via subagente kimi-k2.6 com skill `content-pattern-extractor` |
| Design com Pillow genérico | Design via Canva MCP com template real, ou agente com skill `canva-designer` |
| Entrega Trello via script urllib | Entrega via agente `trello-publisher` com skill injetada |
| Qualidade ruim, sem teste de LLM | Qualidade do LLM mensurada, tiers testados, limites mapeados |

---

## Registro de Incidente

**Data:** 2026-04-29  
**Squad:** carrossel-pattern-extractor (Casa do Bicho)  
**Violação:** Claudinho executou manualmente todo o pipeline em vez de orquestrar agents  
**Impacto:** Nenhum teste real de LLM Ollama; qualidade do entregável abaixo do padrão; nenhum mapeamento de capacity  
**Ação corretiva:** Esta decisão (d_arch_008) + re-execução obrigatória via agents para validar o pipeline real
