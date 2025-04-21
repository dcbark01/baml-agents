from collections.abc import Mapping
from typing import Any

from pydantic import Field

from baml_agents.schema._default_callbacks import (
    DefaultArgsClass,
    DefaultToolClass,
    DefaultToolName,
)
from baml_agents.schema._interfaces import (
    AbstractJsonSchemaToBamlModelConverter,
    AbstractMcpSchemaToBamlModelConverter,
    ArgsClassCallback,
    ToolClassCallback,
    ToolNameCallback,
)
from baml_agents.schema._json_schema_to_baml_model_converter import (
    JsonSchemaToBamlModelConverter,
    JsonSchemaToBamlModelConverterConfig,
)
from baml_agents.schema._model import BamlClassModel, BamlEnumModel


class McpSchemaToBamlModelConverterConfig(JsonSchemaToBamlModelConverterConfig):
    tool_name_field: str = "name"
    tool_args_field: str = "arguments"
    args_class: ArgsClassCallback = Field(default_factory=DefaultArgsClass)
    tool_class: ToolClassCallback = Field(default_factory=DefaultToolClass)
    tool_name: ToolNameCallback = Field(default_factory=DefaultToolName)
    json_schema_converter_cls: type[AbstractJsonSchemaToBamlModelConverter] = Field(
        default=JsonSchemaToBamlModelConverter
    )


class McpSchemaToBamlModelConverter(AbstractMcpSchemaToBamlModelConverter):
    def __init__(
        self,
        schema: str | Mapping[str, Any],
        *,
        config: McpSchemaToBamlModelConverterConfig | None = None,
    ):
        super().__init__(schema)
        self._cfg = config or McpSchemaToBamlModelConverterConfig()

    def convert_tools(self) -> list[BamlClassModel | BamlEnumModel]:
        if "tools" not in self._root_schema:
            raise ValueError("The root schema must contain a 'tools' key.")
        tools: list[dict] = self._root_schema["tools"]

        models = []
        for tool in tools:
            converted = self._convert_tool(tool)
            models.extend(converted)
        return models

    def _convert_tool(self, tool: dict) -> list[BamlClassModel | BamlEnumModel]:
        full_schema = {
            "type": "object",
            "properties": {
                self._cfg.tool_name_field: {
                    "type": "baml_literal_string",  # BAML-specific JSON Schema
                    "baml_literal_string": self._cfg.tool_name(
                        name=tool["name"], schema=tool
                    ),
                }
            },
            "required": [self._cfg.tool_name_field],
        }
        if tool_description := tool.get("description"):
            full_schema["properties"][self._cfg.tool_name_field][
                "description"
            ] = tool_description
        if input_schema := tool.get("inputSchema"):
            full_schema["properties"][self._cfg.tool_args_field] = input_schema
            full_schema["required"].append(self._cfg.tool_args_field)

        tool_class = self._cfg.tool_class(name=tool["name"], schema=tool)
        converter = self._cfg.json_schema_converter_cls(full_schema, tool_class)
        return converter.convert()
