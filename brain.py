#!/usr/bin/env python3
"""
brain.py — Interface CLI simplificada do Claudinho-OpenSquad

Comandos:
    python brain.py start
    python brain.py load <target>
    python brain.py save
    python brain.py status
"""

import sys
import os
import json
import subprocess
from datetime import date

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = os.path.join(PROJECT_DIR, "brain")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def brain_path(*parts):
    return os.path.join(BRAIN_DIR, *parts)


def read_json(*parts):
    path = brain_path(*parts)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print(f"ERROR: Failed to read {'/'.join(parts)}")
        return None


def check_git_repo():
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    return result.returncode == 0


def git_run(args):
    return subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )


# ---------------------------------------------------------------------------
# START
# ---------------------------------------------------------------------------

def handle_start():
    print("Initializing session...\n")

    if not check_git_repo():
        print("ERROR: Not a git repository.")
        return 1

    git_run(["pull"])

    # Carregamento minimo obrigatorio
    meta = read_json("meta", "operational_identity.json")
    policy = read_json("meta", "memory_policy.json")
    protocol = read_json("meta", "session_protocol.json")
    state = read_json("claudinho_state.json")

    if not all([meta, policy, protocol, state]):
        print("ERROR: Failed to load essential context.")
        return 1

    print("Loaded:")
    print("  - meta/operational_identity.json")
    print("  - meta/memory_policy.json")
    print("  - meta/session_protocol.json")
    print("  - claudinho_state.json")

    runtime = state.get("runtime_state", {})
    if runtime.get("_volatile"):
        print("\n⚠  AVISO: runtime_state contem dados volateis.")
        print("   Verifique o estado atual do sistema antes de operar.")
        print(f"   Ultimo registro: {state['meta'].get('last_updated', '?')}")

    print("\n--- State ---")
    print(f"Phase:   {state.get('project_state', {}).get('phase', '?')}")
    print(f"Focus:   {state.get('focus', {}).get('current', '?')}")
    print(f"Status:  {state.get('project_state', {}).get('status', '?')}")

    return 0


# ---------------------------------------------------------------------------
# LOAD
# ---------------------------------------------------------------------------

def handle_load(target):
    if not target:
        print("Usage: python brain.py load <target>")
        return 1

    if target == "decisions":
        index = read_json("decisions", "index.json")
        if index:
            print("Loaded decisions/index.json")
        return 0

    if target == "patterns":
        data = read_json("patterns", "patterns.json")
        if not data:
            return 1
        print("Loaded patterns/patterns.json")
        return 0

    if target == "project":
        index = read_json("projects", "index.json")
        if not index:
            return 1
        print("Loaded projects/index.json")
        return 0

    if target.startswith("decision:"):
        decision_id = target.split(":")[1]
        index = read_json("decisions", "index.json")

        if not index:
            return 1

        for d in index.get("decisions", []):
            if d.get("id") == decision_id:
                file = d.get("file", f"{decision_id}.json")
                read_json("decisions", file)
                print(f"Loaded decisions/{file}")
                return 0

        print("Decision not found.")
        return 1

    print("Unknown target.")
    return 1


# ---------------------------------------------------------------------------
# SAVE
# ---------------------------------------------------------------------------

def handle_save():
    if not check_git_repo():
        print("ERROR: Not a git repository.")
        return 1

    status = git_run(["status", "--porcelain"])

    if not status.stdout.strip():
        print("No changes.")
        return 0

    git_run(["add", "brain/", "brain.py"])

    today = date.today().isoformat()
    msg = f"brain update [{today}]"

    git_run(["commit", "-m", msg])
    git_run(["push"])

    print("Changes saved.")
    return 0


# ---------------------------------------------------------------------------
# STATUS
# ---------------------------------------------------------------------------

def handle_status():
    state = read_json("claudinho_state.json")

    if not state:
        return 1

    print("=== Claudinho-OpenSquad Status ===\n")

    print(f"Phase:   {state.get('project_state', {}).get('phase', '?')}")
    print(f"Status:  {state.get('project_state', {}).get('status', '?')}")
    print(f"Focus:   {state.get('focus', {}).get('current', '?')}")

    blockers = state.get("known_blockers", [])
    if blockers:
        blocker_names = [f"{b.get('id', '?')}: {b.get('description', 'sem descricao')}" for b in blockers]
        print(f"Blockers: {', '.join(blocker_names)}")
    else:
        print("Blockers: none")

    return 0


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Commands: start, load, save, status")
        return 1

    cmd = sys.argv[1]

    if cmd == "start":
        return handle_start()
    elif cmd == "load":
        return handle_load(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "save":
        return handle_save()
    elif cmd == "status":
        return handle_status()
    else:
        print("Unknown command.")
        return 1


if __name__ == "__main__":
    sys.exit(main())