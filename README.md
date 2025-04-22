# baml‑agents

<a href="https://discord.gg/hCppPqm6"><img alt="Discord" src="https://img.shields.io/discord/1119368998161752075?logo=discord&logoColor=white&style=flat"></a>
[![License: MIT](https://img.shields.io/badge/license-MIT-success.svg)](https://opensource.org/licenses/MIT)
<a href="https://badge.fury.io/py/baml-agents"><img src="https://badge.fury.io/py/baml-agents.svg" alt="PyPI version" /></a>
[![status-prototype](https://img.shields.io/badge/status-prototype-yellow.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#experimental)
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>

**Building Agents with [BAML](https://www.boundaryml.com/) for structured generation with LLMs, [MCP Tools](https://modelcontextprotocol.io/docs/concepts/tools), and [12-Factor-Agents](https://github.com/humanlayer/12-factor-agents) principles**

```bash
pip install baml‑agents==0.5.0
```

This repository is intended to share some useful patterns I use while working with BAML. The API is unstable and may change in future versions. Feedback is always welcome!

## Contents

1. [How to use LLM Clients effectively](notebooks/01_llm_clients.ipynb)
   - How to conviently route any of your LLM calls to any LLM provider during runtime
   - What to do if `baml` doesn't support the LLM provider you need (e.g. IBM WatsonX AI, etc.) or an LLM tracing integration you need (e.g. Langfuse, LangSmith, etc.)
   - What to do I can't get `baml` to find the environment variables (e.g. OPENAI_API_KEY, etc.) or I don't want to use them

## Running the Notebooks

To run code from the `notebooks/` folder, you'll first need to:

- Install the [`uv` python package manager](https://docs.astral.sh/uv/).
- Install all dependencies: `uv sync --dev`
- Generates necessary BAML code: `uv run baml-cli generate`
  - Alternatively, you can use the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=Boundary.baml-extension) to do it automatically every time you edit a `.baml` file.
