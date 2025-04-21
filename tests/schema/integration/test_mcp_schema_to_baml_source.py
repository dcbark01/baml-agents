from contextlib import ExitStack

import pytest

from baml_agents.schema._baml_model_to_baml_source_converter import (
    BamlModelToBamlSourceConverter,
)
from baml_agents.schema._mcp_schema_to_baml_model_converter import (
    McpSchemaToBamlModelConverter,
)


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

        baml_models = McpSchemaToBamlModelConverter(schema).convert_tools()
        baml_source = BamlModelToBamlSourceConverter(baml_models).generate()
        actual = baml_source

    # deterministic comparison by sorting on the model name
    assert actual == expected
