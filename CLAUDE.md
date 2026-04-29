# CLAUDE.md — Claudinho-OpenSquad

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mandatory initialization

At the start of every session in this workspace, run:

```bash
python brain.py start
```

This loads Claudinho-OpenSquad's Tier 0 memory (state, meta, evolution log) and displays current system status including blockers, focus, and runtime health.

## Workspace structure

This is the **Claudinho-OpenSquad** repository — a dedicated memory system for the OpenSquad multi-agent framework project.

| Entity | Role | Location |
|---|---|---|
| **Claudinho-OpenSquad** | Builder memory for Claude Code — architectural decisions, patterns, project state | this repo (`claudinho-opensquad/`) |
| **OpenSquad** | The multi-agent orchestration framework being built/adapted | `Desktop/claude-code/` |

### Namespacing rules

- Files in `brain/` belong to the Claudinho-OpenSquad memory system.
- Files in the parent `claude-code/` directory belong to the OpenSquad framework itself.
- **Never** edit OpenSquad core files (`_opensquad/core/`) without understanding the impact on all IDEs.

## Commands

### Claudinho-OpenSquad

Python 3.10+, standard library only — no package manager needed.

```bash
# Initialize session (git pull + validate + load Tier 0)
python brain.py start

# Load selective context
python brain.py load decisions          # decision index
python brain.py load patterns           # validated patterns
python brain.py load decision:d_arch_001 # specific decision

# Persist changes (git add + commit + push)
python brain.py save

# Query state
python brain.py status
```

## High-level architecture

### Tiered memory

**Claudinho-OpenSquad** uses a 4-tier loading system:
- **Tier 0**: `claudinho_state.json` + `meta/` — always loaded (objective, focus, blockers)
- **Tier 1**: `patterns/` — loaded on demand
- **Tier 2**: `decisions/` + `projects/` — loaded on demand
- **Tier 3**: `snapshots/` — only when necessary

### State files

- `brain/claudinho_state.json` — central system state (phase, blockers, focus, runtime status, LLM config).

## Important notes

- This Claudinho is **separate** from the original Claudinho (Hermes/OpenClaw project). Zero knowledge is shared between them.
- The OpenSquad framework lives in the parent `claude-code/` directory.
- All architectural decisions about OpenSquad adaptation (multi-client, model tiers, custom skills) are recorded in `brain/decisions/`.
