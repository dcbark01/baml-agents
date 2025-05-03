import functools
import inspect
from collections.abc import Callable, Sequence
from typing import Any, Generic, TypeVar

from icecream import ic

from baml_agents._baml_hooks._hook_engine import HookEngine
from baml_agents._baml_hooks._hooks._base_hook import BaseBamlHook
from baml_agents._baml_hooks._hooks._types import BamlMutableResult
from baml_agents._utils._sole import sole

T_BamlClient = TypeVar("T_BamlClient")


class BamlClientProxy(Generic[T_BamlClient]):
    """
    A wrapper that intercepts attribute access for a given object.
    It distinguishes between regular and async methods and returns
    a corresponding wrapper that simply calls the original method.
    Non-callable attributes are returned directly.
    """

    def __init__(
        self,
        b: T_BamlClient,
        /,
        *,
        hooks: Sequence[BaseBamlHook] | None = None,
        root_target: T_BamlClient | None = None,
    ):
        object.__setattr__(self, "_passthrough_target", b)
        object.__setattr__(self, "_hooks", hooks)
        object.__setattr__(self, "_root_target", root_target or b)

    def __getattribute__(self, name: str) -> Any:
        # 1. Access internal attributes of the wrapper directly.
        # Use object.__getattribute__ to prevent recursion.
        if name == "request":
            return BamlClientProxy(
                object.__getattribute__(self, "_passthrough_target").request,
                hooks=object.__getattribute__(self, "_hooks"),
                root_target=object.__getattribute__(self, "_passthrough_target"),
            )

        if name in {
            "with_options",
            "__class__",
            "__init__",
            "__getattribute__",
            "__setattr__",
            "__delattr__",
            "__dict__",
            "__dir__",
            "__repr__",
            "__str__",
            # Async/Awaitable checks often look for these
            "__await__",
            "__aiter__",
            "__anext__",
            "__aenter__",
            "__aexit__",
        }:
            try:
                # Get attributes of the wrapper itself first
                return object.__getattribute__(self, name)
            except AttributeError:
                # If the wrapper doesn't have it (e.g., __await__),
                # fall through to get it from the target below.
                pass

        # 2. Get the target object and the requested attribute from it.
        target = object.__getattribute__(self, "_passthrough_target")
        try:
            attr = getattr(target, name)
        except AttributeError:
            # If the target doesn't have the attribute, raise AttributeError naturally.
            # Re-raise the specific error from getattr.
            raise AttributeError(
                f"'{type(target).__name__}' object has no attribute '{name}'"
            ) from None

        # 3. If the attribute is not callable, return it directly.
        if name == "with_options" or not callable(attr):
            return attr

        # 4. If the attribute is callable, determine if it's async or sync.
        if inspect.iscoroutinefunction(attr):
            # Create an ASYNC wrapper
            async def async_wrapper(*args, **kwargs):
                params: dict[str, Any] = object.__getattribute__(
                    self, "_get_baml_function_params"
                )(attr, args, kwargs)
                hook_engine: HookEngine | None = object.__getattribute__(
                    self, "_create_hook_engine"
                )(
                    baml_function_name=name,
                    baml_function_params=params,
                    baml_function_async=True,
                )

                if hook_engine:
                    await hook_engine.on_before_call()

                    result = await attr(**hook_engine.get_baml_function_kwargs())

                    result = BamlMutableResult(baml_function_return_value=result)
                    await hook_engine.on_after_call_success(result)
                else:
                    result = await attr(*args, **kwargs)

                return result

            # Copy metadata
            return functools.wraps(attr)(async_wrapper)

        # Create a SYNC wrapper
        def sync_wrapper(*args, **kwargs):
            params: dict[str, Any] = object.__getattribute__(
                self, "_get_baml_function_params"
            )(attr, args, kwargs)
            hook_engine: HookEngine | None = object.__getattribute__(
                self, "_create_hook_engine"
            )(
                baml_function_name=name,
                baml_function_params=params,
                baml_function_async=False,
            )

            if hook_engine:
                hook_engine.on_before_call_sync()

                result = attr(**hook_engine.get_baml_function_kwargs())

                result = BamlMutableResult(baml_function_return_value=result)
                hook_engine.on_after_call_success_sync(result)
            else:
                result = attr(*args, **kwargs)

            return result

        # Copy metadata
        return functools.wraps(attr)(sync_wrapper)

    # Optional: Proxy __dir__ to make introspection work better
    def __dir__(self):
        target = object.__getattribute__(self, "_passthrough_target")
        # Combine wrapper's dir and target's dir
        return sorted(set(object.__dir__(self)) | set(dir(target)))

    # Optional: Custom repr
    def __repr__(self):
        target = object.__getattribute__(self, "_passthrough_target")
        return f"<_PassthroughWrapper wrapping {target!r}>"

    def _get_baml_function_return_type_name(self, baml_function_name) -> str:
        baml_client = object.__getattribute__(self, "_root_target")
        return (
            getattr(baml_client, baml_function_name).__annotations__["return"].__name__
        )

    def _get_baml_function_params(
        self,
        baml_function: Callable,
        baml_function_args: tuple,
        baml_function_kwargs: dict,
    ) -> dict[str, Any]:
        default_baml_options = sole(
            getattr(object.__getattribute__(self, "_root_target"), attr)
            for attr in dir(object.__getattribute__(self, "_root_target"))
            if attr.endswith("__baml_options")
        )
        print(f"{default_baml_options=}")

        signature = inspect.signature(baml_function)
        bound = signature.bind(*baml_function_args, **baml_function_kwargs)
        bound.apply_defaults()

        baml_options = {
            **default_baml_options,
            **bound.arguments.get("baml_options", {}),
        }
        return {
            **bound.arguments,
            "baml_options": baml_options,
        }

    def _create_hook_engine(
        self,
        baml_function_name: str,
        baml_function_params: dict[str, Any],
        *,
        baml_function_async: bool,
    ) -> HookEngine | None:
        return (
            HookEngine(
                hooks=hooks,
                baml_function_name=baml_function_name,
                baml_function_params=baml_function_params,
                baml_function_async=baml_function_async,
            )
            if (hooks := object.__getattribute__(self, "_hooks"))
            else None
        )

    def with_options(self, **kwargs):
        raise NotImplementedError(
            "Error: You must first set options using 'b.with_options(...)' to create an instance 'b'. Only then can you wrap it with hooks using 'with_hooks(b, [...])' or `with_llm_handler(b, ...)`."
        )
