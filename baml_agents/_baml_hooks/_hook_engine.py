from collections.abc import Sequence
from typing import TYPE_CHECKING

from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHookContext
from baml_agents._baml_hooks._hooks._on_after_call_success_hook import (
    OnAfterCallSuccessHook,
    OnAfterCallSuccessHookContext,
)
from baml_agents._baml_hooks._hooks._on_before_call_hook import (
    OnBeforeCallHook,
    OnBeforeCallHookContext,
)
from baml_agents._baml_hooks._hooks._types import BamlMutableParams, BamlMutableResult

if TYPE_CHECKING:
    from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook


class HookEngine:
    def __init__(
        self,
        *,
        hooks: Sequence["BaseBamlHook"],
        baml_function_name: str,
        baml_function_params: dict,
        baml_function_async: bool,
    ):
        self._hooks = [hook() for hook in hooks]
        self._hook_state = {}
        self._ctx = BaseBamlHookContext(
            baml_function_name=baml_function_name,
            baml_function_return_type=str,
            baml_function_async=baml_function_async,
            hook_state=self._hook_state,
        )
        self._mutable_params = BamlMutableParams(params=baml_function_params)

    def get_baml_function_kwargs(self) -> dict:
        return self._mutable_params.params

    async def on_before_call(self) -> None:
        for hook in self._hooks:
            if isinstance(hook, OnBeforeCallHook):
                ctx = OnBeforeCallHookContext.from_base_context(self._ctx)
                await hook.on_before_call(ctx, self._mutable_params)

    def on_before_call_sync(self) -> None:
        for hook in self._hooks:
            if isinstance(hook, OnBeforeCallHook):
                ctx = OnBeforeCallHookContext.from_base_context(self._ctx)
                hook.on_before_call_sync(ctx, self._mutable_params)

    async def on_after_call_success(self, result: BamlMutableResult) -> None:
        for hook in self._hooks:
            if isinstance(hook, OnAfterCallSuccessHook):
                ctx = OnAfterCallSuccessHookContext.from_base_context(self._ctx)
                await hook.on_after_call_success(ctx, result)

    def on_after_call_success_sync(self, result: BamlMutableResult) -> None:
        for hook in self._hooks:
            if isinstance(hook, OnAfterCallSuccessHook):
                ctx = OnAfterCallSuccessHookContext.from_base_context(self._ctx)
                hook.on_after_call_success_sync(ctx, result)
