from collections.abc import Iterable
from typing import Any, TypeVar

T = TypeVar("T")


def merge_dicts_no_overlap(a: dict[Any, Any], b: dict[Any, Any]) -> dict[Any, Any]:
    """Merge two dicts, error on key collisions."""
    overlap = set(a) & set(b)
    if overlap:
        raise KeyError(f"Collision on keys: {overlap}")
    return {**a, **b}


def sole(items: Iterable[T]) -> T:
    lst = list(items)
    if len(lst) != 1:
        raise ValueError(f"Expected single element, got {len(lst)}")
    return lst[0]


def snake_to_pascal(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    return "".join(word.capitalize() for word in name.replace("-", "_").split("_"))
