from typing import Any

from pydantic import BaseModel


class BamlMutableResult(BaseModel):
    baml_function_return_value: Any


class BamlMutableParams(BaseModel):
    params: dict[str, Any]
