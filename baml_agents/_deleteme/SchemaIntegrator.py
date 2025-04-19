from typing import Any, Iterable

from baml_py.type_builder import TypeBuilder
from pydantic_ai.tools import ToolDefinition

from baml_agents._mcp._tool_to_baml_type import tool_to_baml_type


class SchemaIntegrator:
    """Integrate tool types into BAML output model."""

    def __init__(
        self,
        builder: TypeBuilder,
        output_model: Any,
        tools: Iterable[ToolDefinition],
        field: str = "intents",
    ) -> None:
        types = [tool_to_baml_type(t, builder) for t in tools]
        output_model.add_property(field, builder.list(builder.union(types)))
        self.field = field

    def property_field(self) -> str:
        """Return the tools field name."""
        return self.field
