from collections.abc import Mapping
from typing import Any, Protocol, Self

from pydantic import BaseModel, ConfigDict, Field


class BaseBamlHookContext(BaseModel):
    baml_function_name: str
    baml_function_return_type: type
    baml_function_async: bool
    baml_function_options: dict[str, Any] = Field(default_factory=dict)

    # Shared mutable state dictionary for communication between hooks
    hook_state: Mapping[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @classmethod
    def from_base_context(cls, base_context: "BaseBamlHookContext") -> Self:
        return cls(**base_context.model_dump())


class BaseBamlHook(Protocol):
    def __call__(self) -> Self:
        """
        # If your hook maintains state, consider using a factory class
        # instead of directly instantiating the hook. This approach ensures
        # that each call results in a new, clean hook state.
        """
        return self
