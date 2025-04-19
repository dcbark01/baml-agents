# baml‑agents

**12‑Factor AI Agents: BAML‑powered structured generation & plug‑and‑play MCP tools**

```bash
pip install baml‑agents
```

## What you get

- **Robust architecture** – follows the [12‑Factor Agents](https://github.com/humanlayer/12-factor-agents) principles.
- **Structured generation** – BAML enforces structured outputs.
- **Zero‑friction tools** – `pydantic‑ai‑slim[mcp]` lets you use BAML to let LLMs call local (Python) or remote (MCP) tools with a single unified interface.

## Quick start

```bash
# prerequisites
uv pip install baml‑agents
uv run baml-cli generate   # scaffolds the baml_client folder
```

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) CLI
