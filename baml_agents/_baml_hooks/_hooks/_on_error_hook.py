from typing import Protocol, final

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook, BaseBamlHookContext


@final
class OnErrorHookContext(BaseBamlHookContext):
    error: Exception


class OnErrorHook(BaseBamlHook, Protocol):
    async def on_error(self, context: OnErrorHookContext) -> None:
        self.on_error_sync(context)

    def on_error_sync(self, context: OnErrorHookContext) -> None:
        raise NotImplementedError("on_error_sync is not implemented.")
