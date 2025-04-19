# baml‑agents

**12‑Factor AI Agents: BAML‑powered structured generation & plug‑and‑play MCP tools**

```bash
pip install baml‑agents
```

## What you get

- **Robust architecture** – follows the [12‑Factor Agents](https://github.com/humanlayer/12-factor-agents) principles.
- **Structured generation** – BAML enforces structured outputs.
- **Zero‑friction tools** – `pydantic‑ai‑slim[mcp]` enables LLMs to call local (Python) or remote (MCP) tools through a unified interface.

## Why wrap tools in the MCP format?

Even if your tools are purely internal, wrapping them in MCP offers significant design advantages:

- **Transport‑agnostic integration**  
  MCP typically uses _http/sse_ or _stdio_ for separate‑process communication, but we can also support direct in‑process Python function calls—providing a zero‑overhead, low‑latency integration without the need for external servers.

- **Hot‑swappable deployments**  
  Seamlessly switch between in‑process (inner) and remote (outer) tool implementations without modifying prompts or model code.

- **Framework‑agnostic agents**  
  Easily replace or upgrade your agent core (e.g., switching LLM backends or orchestration frameworks) without rewriting tool interfaces.

- **Cross‑project reuse**  
  Define tools once within an MCP server and reuse them across multiple applications and teams, avoiding redundant logic.

- **Effortless externalization at scale**  
  As your demand grows, migrate tools from local execution to dedicated services or clusters without altering client code or model configurations.

## Getting Started

Explore the `notebooks/` folder for practical examples.

## Running example notebooks

Prerequisites:
- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) CLI
```bash
uv sync --dev
uv run baml-cli generate
```
