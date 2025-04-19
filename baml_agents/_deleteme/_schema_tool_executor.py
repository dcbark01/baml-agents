from __future__ import annotations

from typing import Any, Dict, Iterable, List, TypeVar

from baml_py.type_builder import TypeBuilder
from pydantic_ai.tools import ToolDefinition

from baml_agents._mcp.SchemaIntegrator import SchemaIntegrator
from baml_agents._mcp.ToolExecutor import ToolExecutor
from baml_agents._mcp.ToolRegistry import ToolRegistry
from baml_agents._mcp.used_tool import UsedTool

T = TypeVar("T")


class SchemaToolExecutor:
    """Facade: integrate schema and execute tools in BAML workflows."""

    def __init__(
        self,
        builder: TypeBuilder,
        output_model: Any,
        tools: Iterable[ToolDefinition],
        registry: ToolRegistry,
        field: str = "intents",
    ) -> None:
        self.integrator = SchemaIntegrator(builder, output_model, tools, field)
        self.executor = ToolExecutor(registry)
        self.field = field

    def select(self, resp: Any) -> List[Dict[str, Any]]:
        if sel := getattr(resp, self.field, None):
            return sel
        if isinstance(resp, dict) and "tool_id" in resp:
            return [resp]
        raise ValueError("No tools selected in response")

    async def run(self, resp: Any) -> List[UsedTool]:
        selected = self.select(resp)
        return await self.executor.execute(selected)
