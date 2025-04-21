from collections.abc import Iterable
from typing import TypeVar

from baml_py.type_builder import TypeBuilder

from baml_agents.deprecated.pydantic_mcp._import import pydantic_import_err_msg

try:
    from pydantic_ai.tools import ToolDefinition  # type: ignore
except ImportError as e:
    raise ImportError(pydantic_import_err_msg) from e

from baml_agents.deprecated.pydantic_mcp._baml_tool_prompt_config import (
    BamlToolPromptConfig,
)
from baml_agents.deprecated.pydantic_mcp._tool_to_baml_type import (
    AbstractToolToBamlType,
)

T = TypeVar("T", bound=TypeBuilder)


class TypeBuilderOrchestrator:
    """Builds BAML types from ToolDefinitions and attaches them to an output class."""

    def __init__(
        self,
        *,
        tool_converter: AbstractToolToBamlType,
        prompt_cfg: BamlToolPromptConfig,
    ):
        self._converter = tool_converter
        self._prompt_cfg = prompt_cfg

    async def build_types(
        self,
        tb: T,
        output_class,
        *,
        tools: Iterable[ToolDefinition],
    ) -> T:
        baml_types = [
            self._converter.convert(
                tool=t,
                tb=tb,
                baml_tool_id_field=self._prompt_cfg.id_field,
            )
            for t in tools
        ]
        union = tb.union(baml_types)
        if self._prompt_cfg.can_select_many:
            union = union.list()
        output_class.add_property(self._prompt_cfg.tools_field, union)
        return tb
