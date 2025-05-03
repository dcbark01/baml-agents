from typing import Protocol, final

from typing_extensions import runtime_checkable

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook, BaseBamlHookContext
from baml_agents._baml_hooks._hooks._types import BamlMutableParams


@final
class OnBeforeCallHookContext(BaseBamlHookContext):
    pass


@runtime_checkable
class OnBeforeCallHook(BaseBamlHook, Protocol):
    async def on_before_call(
        self,
        context: OnBeforeCallHookContext,
        mutable_args: BamlMutableParams,
    ) -> None:
        self.on_before_call_sync(context, mutable_args)

    def on_before_call_sync(
        self,
        context: OnBeforeCallHookContext,
        mutable_args: BamlMutableParams,
    ) -> None:
        raise NotImplementedError("on_before_call_sync is not implemented. ")
