from baml_agents.schema._interfaces import AbstractMcpSchemaToBamlModelConverter
from baml_agents.schema._model import BamlClassModel, BamlEnumModel


class McpSchemaToBamlModelConverter(AbstractMcpSchemaToBamlModelConverter):
    """
    Abstract base class for MCP JSON Schema to BAML model converters.
    Defines the public interface expected for all concrete converters.
    """

    def convert(self) -> list[BamlClassModel | BamlEnumModel]:
        """
        Converts the loaded MCP JSON schema to a list of BAML model dataclasses.

        Returns:
            List of BamlClassModel and BamlEnumModel instances.

        """
        return []
