from typing import Protocol, final

from typing_extensions import runtime_checkable

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook, BaseBamlHookContext
from baml_agents._baml_hooks._hooks._types import BamlMutableResult


@final
class OnAfterCallSuccessHookContext(BaseBamlHookContext):
    pass


@runtime_checkable
class OnAfterCallSuccessHook(BaseBamlHook, Protocol):
    async def on_after_call_success(
        self,
        context: OnAfterCallSuccessHookContext,
        mutable_result: BamlMutableResult,
    ) -> None:
        self.on_after_call_success_sync(context, mutable_result)

    def on_after_call_success_sync(
        self,
        context: OnAfterCallSuccessHookContext,
        mutable_result: BamlMutableResult,
    ) -> None:
        raise NotImplementedError("on_after_call_success_sync is not implemented.")
