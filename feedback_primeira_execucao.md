---
name: feedback_primeira_execucao_pipeline
description: Feedback honesto sobre a primeira execucao do pipeline de carrossel — o que funcionou, o que ficou ruim, e o que precisa mudar
type: feedback
---

## Feedback: Primeira Execucao do Pipeline (Carrossel Luna)

**Data:** 2026-04-29
**Squad:** carrossel-pattern-extractor (Casa do Bicho)

### O que funcionou (infraestrutura)
- MCPs conectam e respondem (Playwright, Apify, Tavily, Trello, Canva)
- Apify extrai dados do Instagram com sucesso
- Trello recebe cards via API
- Pillow gera imagens PNG localmente
- Estrutura de diretorios multi-cliente organizada

### O que ficou ruim (qualidade)

**1. Mapeamento de padroes — RUIM**
- Pattern extractor usou apenas captions do Apify (frequentemente vazios/truncados para carrosseis)
- Nao houve analise real do conteudo dos slides, arquitetura visual, elementos graficos
- Relatorio gerado e generico — aplicavel a qualquer nicho com mudancas superficiais
- Nao extraiu o que faz o leitor parar o scroll

**2. Angulos gerados — OBVIOS E GENERICOS**
- "Antes/depois de pelagem" e o basico do marketing pet
- Nao aplicou o padrao sofisticado dos 39K likes (analise de tendencia + escassez)
- Gancho fraco, sem pattern interrupt real
- CTA "comenta LUNA" oferece recompensa insuficiente
- Copy de agencia generica, nao de quem entende o nicho pet de Ilheus

**3. Design — WIREFRAME, NAO ENTREGAVEL**
- Retangulo branco + texto preto + circulo verde
- Sem hierarquia visual, branding, elementos graficos
- Nao explorou contraste, peso tipografico, direcao de leitura
- Comparado ao template X Carousel indicado: embrionario

### O que NAO foi testado (e deveria ter sido)

**4. Subagents com LLMs Ollama — NUNCA EXECUTADOS**
- Todo o trabalho foi feito manualmente pelo Claude Code (modelo Anthropic)
- Pattern extractor rodou em Python puro, nao em agente LLM
- Angulos foram escritos por mim, nao gerados por glm-5.1 ou kimi-k2.6
- Nao mapeamos latencia, timeouts, rate limits, nem capacidade dos modelos locais

**5. Switch de model tiers — NAO ACIONADO**
- Nao houve execucao multi-agente automatizada
- Nao sabemos se glm-5.1 consegue pattern extraction
- Nao sabemos se kimi-k2.6 consegue gerar angulos criativos de verdade
- O mapeamento fast/powerful existe no papel, mas nunca foi exercitado

### Proxima abordagem sugerida

1. **Pattern extraction:** Usar LLM (kimi-k2.6) para analisar manualmente os dados do Apify, slide por slide, com prompt estruturado — nao confiar em heuristica Python
2. **Angle generation:** Testar com glm-5.1 primeiro (rapido) para esboco, depois kimi-k2.6 (profundo) para refinamento — exercitar o switch de tiers
3. **Design:** Usar Canva MCP com template real na conta do usuario, nao Pillow generico
4. **Pipeline:** Executar como squad real com agents Ollama, nao manualmente

**Regra para lembrar:** PoC de infraestrutura != PoC de qualidade de entrega. Testar conectividade nao prova que o produto final e bom.
