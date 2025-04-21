from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeVar, runtime_checkable

from baml_agents.schema._model import BamlClassModel, BamlEnumModel

if TYPE_CHECKING:
    from baml_py.type_builder import TypeBuilder

T = TypeVar("T", bound="TypeBuilder")


class AbstractMcpSchemaToBamlModelConverter(ABC):
    """
    Abstract base class for MCP JSON Schema to BAML model converters.
    Defines the public interface expected for all concrete converters.
    """

    @abstractmethod
    def convert(self) -> list[BamlClassModel | BamlEnumModel]:
        """
        Converts the loaded MCP JSON schema to a list of BAML model dataclasses.

        Returns:
            List of BamlClassModel and BamlEnumModel instances.

        """


class AbstractJsonSchemaToBamlModelConverter(ABC):
    """
    Abstract base class for JSON Schema to BAML model converters.
    Defines the public interface expected for all concrete converters.
    """

    @abstractmethod
    def convert(self) -> list[BamlClassModel | BamlEnumModel]:
        """
        Converts the loaded JSON schema to a list of BAML model dataclasses.

        Returns:
            List of BamlClassModel and BamlEnumModel instances.

        """


class BamlGenerator(ABC, Generic[T]):
    """Abstract base for generating BAML source code or TypeBuilder objects."""

    @abstractmethod
    def generate_baml_source(self) -> str:
        """
        Generate BAML source code.

        :return: BAML source code as a string.
        """

    @abstractmethod
    def add_to_type_builder(self, tb: T) -> T:
        """
        Add types/classes into the provided TypeBuilder.

        :param tb: An instance of TypeBuilder to which types will be added.
        :return: The same TypeBuilder instance (return is for convenience; the object is mutated in place).
        """


@runtime_checkable
class ArgsClassCallback(Protocol):
    def __call__(
        *,
        name: str,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str: ...


@runtime_checkable
class ToolClassCallback(Protocol):
    def __call__(
        *,
        name: str,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str: ...


@runtime_checkable
class ToolNameCallback(Protocol):
    def __call__(
        *,
        name: str,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str: ...


@runtime_checkable
class PropNameCallback(Protocol):
    def __call__(
        *,
        name: str,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str: ...


@runtime_checkable
class DescCallback(Protocol):
    def __call__(
        *,
        description: str | None,
        root: bool,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str | None: ...


@runtime_checkable
class AliasCallback(Protocol):
    def __call__(
        *,
        name: str,
        root: bool,
        prop_schema: dict[str, Any],
        class_schema: dict[str, Any],
        root_class_schema: dict[str, Any],
    ) -> str | None: ...
