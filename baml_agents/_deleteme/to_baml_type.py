from typing import Any, Dict

from baml_py.type_builder import TypeBuilder

from baml_agents._mcp._json_schema_to_baml_converter import JsonSchemaToBamlConverter


def to_baml_type(schema: Dict[str, Any], builder: TypeBuilder) -> FieldType:
    """Convert JSON schema dict to BAML FieldType."""
    return
