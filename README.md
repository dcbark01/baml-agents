# baml‑agents

**12‑Factor AI Agents: BAML‑powered structured generation & plug‑and‑play MCP tools**

```bash
pip install baml‑agents
```

## What you get

- **Robust architecture** – follows the [12‑Factor Agents](https://github.com/humanlayer/12-factor-agents) principles.
- **Structured generation** – BAML enforces structured outputs.
- **Zero‑friction tools** – pydantic‑ai‑slim[mcp] lets you use BAML to let LLMs call local (Python) or remote (MCP) tools with a single unified interface.

## Why wrap tools in the MCP format?

Even if your tools are purely internal, wrapping them in MCP delivers key design advantages:

1. **Hot‑swappable deployments**  
   Swap between in‑process (inner) and remote (outer) tool implementations without touching prompts or model code.

2. **Framework‑agnostic agents**  
   Replace or upgrade your agent core (e.g., switch LLM backends or orchestration frameworks) without rewriting tool interfaces.

3. **Cross‑project reuse**  
   Define a tool once on an MCP server and share it across multiple applications and teams, avoiding duplicated logic.

4. **Smooth externalization at scale**  
   As demand grows, migrate a tool from local execution to a dedicated service or cluster without changing client code or model configurations.

## Getting Started

Check the `notebooks/` folder for examples.

## Running example notebooks

Prerequisites:

```bash
uv sync --dev
uv run baml-cli generate
```

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) CLI
