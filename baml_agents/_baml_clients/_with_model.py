import os
from typing import TypeVar

from ._with_client import with_client

T = TypeVar("T")


def with_model(b: T, model: str) -> T:
    provider = "openai"
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_API_BASE")

    options = {
        "model": model,
        "api_key": api_key,
    }
    if base_url:
        options["base_url"] = base_url
    return with_client(b, provider=provider, options=options)  # type: ignore

