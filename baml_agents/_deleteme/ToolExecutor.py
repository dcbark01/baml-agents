import asyncio
import json
from typing import Any, Dict, List

from mcp.types import CallToolResult

from baml_agents._mcp.Sole import Sole
from baml_agents._mcp.ToolRegistry import ToolRegistry


class ToolExecutor:
    """Execute selected tools against a registry."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    async def execute(
        self,
        selected: List[Dict[str, Any]],
    ) -> List[UsedTool]:
        tasks = [
            self.registry.call_tool(
                item["tool_id"], {k: v for k, v in item.items() if k != "tool_id"}
            )
            for item in selected
        ]
        results = await asyncio.gather(*tasks)
        return [self._wrap(item, res) for item, res in zip(selected, results)]

    @staticmethod
    def _wrap(item: Dict[str, Any], res: CallToolResult) -> UsedTool:
        c = Sole.one(res.content)
        if c.type != "text":
            raise TypeError(f"Unexpected content: {c.type}")
        if res.isError:
            raise RuntimeError(f"Tool error: {c.text}")
        return UsedTool(tool_input=json.dumps(item, indent=2), tool_output=c.text)
