from collections.abc import Awaitable, Callable
from typing import Any, Protocol, final

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook, BaseBamlHookContext
from baml_agents._baml_hooks._hooks._types import BamlMutableResult

PartialCallback = Callable[[Any], Awaitable[None]] | None


@final
class HandleLlmInteractionHookContext(BaseBamlHookContext):
    pass


class HandleLlmInteractionHook(BaseBamlHook, Protocol):
    async def handle_llm_interaction(
        self,
        context: HandleLlmInteractionHookContext,
        mutable_result: BamlMutableResult,
    ) -> None:
        self.handle_llm_interaction_sync(context, mutable_result)

    def handle_llm_interaction_sync(
        self,
        context: HandleLlmInteractionHookContext,
        mutable_result: BamlMutableResult,
    ) -> None:
        raise NotImplementedError("handle_llm_interaction_sync is not implemented.")
