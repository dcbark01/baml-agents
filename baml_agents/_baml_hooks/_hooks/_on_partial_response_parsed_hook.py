from typing import Any, Protocol, final

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook, BaseBamlHookContext


@final
class OnPartialResponseParsedHookContext(BaseBamlHookContext):
    partial_result: Any


class OnPartialResponseParsedHook(BaseBamlHook, Protocol):
    async def on_partial_response_parsed(
        self,
        context: OnPartialResponseParsedHookContext,
    ) -> None:
        self.on_partial_response_parsed_sync(context)

    def on_partial_response_parsed_sync(
        self,
        context: OnPartialResponseParsedHookContext,
    ) -> None:
        raise NotImplementedError("on_partial_response_parsed_sync is not implemented.")
