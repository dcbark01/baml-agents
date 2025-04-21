from contextlib import ExitStack

import pytest

from baml_agents.schema._baml_model_to_type_builder_converter import (
    BamlModelToTypeBuilderConverter,
)
from baml_agents.schema._mcp_schema_to_baml_model_converter import (
    McpSchemaToBamlModelConverter,
)
from baml_agents.utils._baml import get_payload
from baml_client.sync_client import b
from baml_client.type_builder import TypeBuilder


@pytest.mark.parametrize(
    "schema, expected, expected_warnings",
    [
        pytest.param(
            {
                "tools": [
                    {
                        "description": "Calculates/evaluates the given expression.",
                        "inputSchema": {
                            "properties": {
                                "expression": {"title": "Expression", "type": "string"}
                            },
                            "required": ["expression"],
                            "title": "calculateArguments",
                            "type": "object",
                        },
                        "name": "calculate",
                    }
                ]
            },
            """\
class CalculateTool {
  name literal_string @description(#"Calculates/evaluates the given expression."#)
  arguments CalculateArguments
}

class CalculateArguments {
  expression str
}
""",
            None,
            id="uvx mcp-server-calculator",
        ),
    ],
)
def test_mcp_schema_to_baml_source(
    schema,
    expected: str,
    expected_warnings,
):
    with ExitStack() as stack:
        # enter a pytest.warns context for each expected warning;
        # if expected_warnings is empty or None, the loop simply does nothing
        for warning_type, match_regex in expected_warnings or []:
            stack.enter_context(pytest.warns(warning_type, match=match_regex))

        from_mcp = McpSchemaToBamlModelConverter(schema)
        baml_models = from_mcp.convert_tools()
        tb = TypeBuilder()
        to_baml_source = BamlModelToTypeBuilderConverter(baml_models).configure(tb)
        tb.MyClass.add_property()
        actual = get_payload(b.request.RenderMyClass())

    # deterministic comparison by sorting on the model name
    assert actual == expected
