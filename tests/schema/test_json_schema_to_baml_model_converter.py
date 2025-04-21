from contextlib import ExitStack

import pytest

from baml_agents.schema._json_schema_to_baml_model_converter import (
    JsonSchemaToBamlModelConverter,
)
from baml_agents.schema._model import (
    BamlBaseType,
    BamlClassModel,
    BamlEnumModel,
    BamlEnumValueModel,
    BamlFieldModel,
    BamlTypeInfo,
)


@pytest.mark.parametrize(
    "class_name, schema, expected,expected_warnings",
    [
        pytest.param(
            "calculate_expression",
            {
                "properties": {"expression": {"title": "Expression", "type": "string"}},
                "required": ["expression"],
                "title": "calculateArguments",
                "type": "object",
            },
            [
                BamlClassModel(
                    name="CalculateExpression",
                    properties=[
                        BamlFieldModel(
                            name="expression",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                    ],
                    alias="calculateArguments",
                ),
            ],
            None,
            id="uvx mcp-server-calculator",
        ),
        pytest.param(
            "search_papers",
            {
                "properties": {
                    "categories": {
                        "items": {"type": "string"},
                        "type": "array",
                    },
                    "date_from": {"type": "string"},
                    "date_to": {"type": "string"},
                    "max_results": {"type": "integer"},
                    "query": {"type": "string"},
                },
                "required": ["query"],
                "type": "object",
            },
            [
                BamlClassModel(
                    name="SearchPapers",
                    properties=[
                        BamlFieldModel(
                            name="categories",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.LIST,
                                item_type=BamlTypeInfo(
                                    base_type=BamlBaseType.STR,
                                ),
                                is_optional=True,
                            ),
                        ),
                        BamlFieldModel(
                            name="dateFrom",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                            alias="date_from",
                        ),
                        BamlFieldModel(
                            name="dateTo",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                            alias="date_to",
                        ),
                        BamlFieldModel(
                            name="maxResults",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.INT,
                                is_optional=True,
                            ),
                            alias="max_results",
                        ),
                        BamlFieldModel(
                            name="query",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                    ],
                ),
            ],
            None,
            id="uvx mcp-server-arxiv",
        ),
        pytest.param(
            "SimpleString",
            {"type": "string"},
            [],  # No models expected for a simple root type
            None,
            id="simple_string",
        ),
        pytest.param(
            "OptionalString",
            {"type": ["string", "null"]},
            [],  # No models expected for a simple root type
            None,
            id="optional_string",
        ),
        pytest.param(
            "StringEnum",
            {"type": "string", "enum": ["a", "b-c", "d"]},
            # Expect an Enum model to be generated for the root type if it's an enum
            [
                BamlEnumModel(
                    name="AnonymousEnum1",
                    values=[
                        BamlEnumValueModel(name="A", alias="a", skip=False),
                        BamlEnumValueModel(name="BC", alias="b-c", skip=False),
                        BamlEnumValueModel(name="D", alias="d", skip=False),
                    ],
                )
            ],
            [(UserWarning, r"Assigning anonymous name 'AnonymousEnum1'")],
            id="string_enum",
        ),
        pytest.param(
            "Anonymous",  # No title, so class name is derived from input
            {"type": "object", "properties": {"prop": {"type": "integer"}}},
            [
                BamlClassModel(
                    name="Anonymous",
                    properties=[
                        BamlFieldModel(
                            name="prop",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.INT,
                                is_optional=True,
                            ),
                        )
                    ],
                )
            ],
            None,
            id="object_no_title",
        ),
        pytest.param(
            "RootArray",  # Root is an array, models are generated for the item type
            {
                "type": "array",
                "items": {
                    "type": "object",
                    "title": "Item",  # Title used for class name
                    "properties": {"id": {"type": "number"}},  # number maps to float
                },
            },
            [
                BamlClassModel(
                    name="Item",
                    properties=[
                        BamlFieldModel(
                            name="id",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.FLOAT,
                                is_optional=True,
                            ),
                        )
                    ],
                )
            ],
            None,
            id="array_of_objects",
        ),
        pytest.param(
            "RefToPrimitive",
            {
                "type": "object",
                "properties": {"name": {"$ref": "#/$defs/name_def"}},
                "$defs": {"name_def": {"type": "string"}},
            },
            # The root object itself becomes a class
            [
                BamlClassModel(
                    name="RefToPrimitive",
                    properties=[
                        BamlFieldModel(
                            name="name",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                        )
                    ],
                )
            ],
            None,
            id="ref_to_primitive",
        ),
        pytest.param(
            "UnionRoot",
            {
                "anyOf": [{"type": "string"}, {"$ref": "#/$defs/Address"}],
                "$defs": {
                    "Address": {
                        "type": "object",
                        "title": "Address",
                        "properties": {"street": {"type": "string"}},
                    },
                },
            },
            # Models are generated for the definitions ($defs)
            # The root union itself doesn't generate a top-level model here, but the referenced Address does.
            # The duplicate might indicate an issue in handling how $refs are processed in unions/anyOf vs direct use.
            [
                BamlClassModel(
                    name="Address",
                    properties=[
                        BamlFieldModel(
                            name="street",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                        )
                    ],
                ),
                BamlClassModel(
                    name="Address",
                    properties=[
                        BamlFieldModel(
                            name="street",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                        )
                    ],
                ),
            ],
            None,
            id="union_object_or_string",
        ),
        pytest.param(
            "Node",
            {
                "title": "Node",
                "type": "object",
                "properties": {
                    "value": {"type": "integer"},
                    "next": {"$ref": "#"},
                },  # Self reference
            },
            [
                BamlClassModel(
                    name="Node",
                    properties=[
                        BamlFieldModel(
                            name="value",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.INT,
                                is_optional=True,
                            ),
                        ),
                        BamlFieldModel(
                            name="next",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.CLASS,
                                custom_type_name="Node",
                                is_optional=True,
                            ),
                        ),
                    ],
                )
            ],
            [
                (
                    UserWarning,
                    r"Could not find BamlClassModel 'Node' to cache for \$ref '#'",
                )
            ],
            id="circular_ref",
        ),
        pytest.param(
            "UserProfile",
            {
                "title": "UserProfile",
                "description": "Represents a user profile with address and preferences.",
                "type": "object",
                "required": ["userId", "email", "preferences"],
                "properties": {
                    "userId": {
                        "type": "string",
                        "description": "Unique identifier for the user.",
                    },
                    "email": {"type": "string", "format": "email"},
                    "displayName": {
                        "type": ["string", "null"],
                        "description": "Optional display name",
                    },
                    "address": {"$ref": "#/$defs/Address"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of user tags.",
                    },
                    "preferences": {
                        "type": "object",
                        "title": "UserPreferences",  # Nested object with title -> becomes a class
                        "properties": {
                            "theme": {"$ref": "#/$defs/ThemeEnum"},
                            "notificationsEnabled": {
                                "type": "boolean",
                                "default": True,  # Default doesn't affect BAML model structure
                            },
                        },
                        "required": ["theme"],
                    },
                    "metadata": {
                        "type": "object",
                        "additionalProperties": True,
                    },  # Becomes a class, additionalProperties handled separately
                    "previousAddresses": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/Address"},  # Array of references
                    },
                    "status": {
                        "type": ["string", "null"],
                        "enum": [
                            "active",
                            "inactive",
                            "pending",
                            None,
                        ],  # Nullable enum - BAML handles this as optional string for now
                    },
                },
                "$defs": {
                    "Address": {
                        "type": "object",
                        "title": "Address",
                        "properties": {
                            "street": {"type": "string"},
                            "city": {"type": "string"},
                            "zipCode": {
                                "type": "string",
                                "pattern": "\\d{5}",
                            },  # Pattern doesn't affect BAML model
                        },
                        "required": ["street", "city", "zipCode"],
                    },
                    "ThemeEnum": {
                        "title": "InterfaceTheme",
                        "type": "string",
                        "description": "The UI theme preference.",
                        "enum": ["dark", "light", "system"],
                    },
                },
            },
            [
                BamlClassModel(
                    name="UserProfile",
                    properties=[
                        BamlFieldModel(
                            name="userId",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                            description="Unique identifier for the user.",
                        ),
                        BamlFieldModel(
                            name="email",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                        BamlFieldModel(
                            name="displayName",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                            description="Optional display name",
                        ),
                        BamlFieldModel(
                            name="address",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.CLASS,
                                custom_type_name="Address",
                                is_optional=True,
                            ),
                        ),
                        BamlFieldModel(
                            name="tags",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.LIST,
                                item_type=BamlTypeInfo(
                                    base_type=BamlBaseType.STR,
                                ),
                                is_optional=True,
                            ),
                            description="List of user tags.",
                        ),
                        BamlFieldModel(
                            name="preferences",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.CLASS,
                                custom_type_name="UserPreferences",
                            ),
                        ),
                        BamlFieldModel(
                            name="metadata",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.CLASS,
                                custom_type_name="Metadata",
                                is_optional=True,
                            ),
                        ),
                        BamlFieldModel(
                            name="previousAddresses",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.LIST,
                                item_type=BamlTypeInfo(
                                    base_type=BamlBaseType.CLASS,
                                    custom_type_name="Address",
                                ),
                                is_optional=True,
                            ),
                        ),
                        BamlFieldModel(
                            name="status",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                                is_optional=True,
                            ),
                        ),
                    ],
                    description="Represents a user profile with address and preferences.",
                ),
                BamlClassModel(
                    name="Address",
                    properties=[
                        BamlFieldModel(
                            name="street",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                        BamlFieldModel(
                            name="city",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                        BamlFieldModel(
                            name="zipCode",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                    ],
                ),
                BamlClassModel(
                    name="Address",
                    properties=[
                        BamlFieldModel(
                            name="street",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                        BamlFieldModel(
                            name="city",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                        BamlFieldModel(
                            name="zipCode",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.STR,
                            ),
                        ),
                    ],
                ),  # Duplicate Address - likely from being referenced multiple times (direct + list)
                BamlClassModel(
                    name="UserPreferences",
                    properties=[
                        BamlFieldModel(
                            name="theme",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.ENUM,
                                custom_type_name="InterfaceTheme",
                            ),
                        ),
                        BamlFieldModel(
                            name="notificationsEnabled",
                            type_info=BamlTypeInfo(
                                base_type=BamlBaseType.BOOL,
                                is_optional=True,
                            ),
                        ),
                    ],
                ),
                BamlEnumModel(
                    name="InterfaceTheme",
                    values=[
                        BamlEnumValueModel(name="Dark", alias="dark", skip=False),
                        BamlEnumValueModel(name="Light", alias="light", skip=False),
                        BamlEnumValueModel(name="System", alias="system", skip=False),
                    ],
                    description="The UI theme preference.",
                ),
                BamlEnumModel(
                    name="InterfaceTheme",
                    values=[
                        BamlEnumValueModel(name="Dark", alias="dark", skip=False),
                        BamlEnumValueModel(name="Light", alias="light", skip=False),
                        BamlEnumValueModel(name="System", alias="system", skip=False),
                    ],
                    description="The UI theme preference.",
                ),  # Duplicate Enum - likely from being referenced inside UserPreferences
                BamlClassModel(
                    name="Metadata",
                    properties=[],
                ),  # Class for the additionalProperties object
            ],
            [
                (
                    UserWarning,
                    r"Schema at '#/properties/metadata' uses 'additionalProperties: true'",
                )
            ],
            id="complex",
        ),
    ],
)
def test_json_schema_to_baml_model_converter(
    class_name,
    schema,
    expected: list[BamlClassModel | BamlEnumModel],
    expected_warnings,
):
    converter = JsonSchemaToBamlModelConverter(schema)

    with ExitStack() as stack:
        # enter a pytest.warns context for each expected warning;
        # if expected_warnings is empty or None, the loop simply does nothing
        for warning_type, match_regex in expected_warnings or []:
            stack.enter_context(pytest.warns(warning_type, match=match_regex))

        actual = converter.convert(class_name)

    # deterministic comparison by sorting on the model name
    actual_sorted = sorted(actual, key=lambda m: m.name)
    expected_sorted = sorted(expected, key=lambda m: m.name)

    assert actual_sorted == expected_sorted, f"Conversion mismatch for {class_name}"
