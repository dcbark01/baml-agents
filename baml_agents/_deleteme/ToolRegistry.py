from types import TracebackType
from typing import Any, Dict, List, Protocol, runtime_checkable

from mcp.types import CallToolResult
from pydantic_ai.tools import ToolDefinition


@runtime_checkable
class ToolRegistry(Protocol):
    """Interface for listing and invoking tools."""

    async def list_tools(self) -> List[ToolDefinition]: ...
    async def call_tool(self, name: str, args: Dict[str, Any]) -> CallToolResult: ...
    async def __aenter__(self) -> ToolRegistry: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None: ...
