import re
from dataclasses import dataclass
from typing import Any, List

from pydantic import BaseModel, ConfigDict

from baml_client.types import Interaction
from baml_agents._agent_tools._action import (
    Action,
)  # Use specific types for Action and Result if known


def print_result(result):
    completion = result.calls[0].http_response.body.json()["choices"][0]["message"][  # type: ignore
        "content"
    ]
    model = result.calls[0].http_response.body.json()["model"]  # type: ignore
    clean_completion = re.sub(r"\s+", "", completion)
    print(f"Model: {model}\nReturned: {clean_completion}")


def city_to_number(city: str, min_value: int, max_value: int) -> int:
    """
    Deterministically map a city name to an integer in the range [min_value, max_value].
    """
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    city_hash = abs(hash(city.lower()))
    range_size = max_value - min_value + 1
    return (city_hash % range_size) + min_value


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def city_to_weather_condition(city: str) -> str:
    """
    Deterministically map a city name to a weather condition.
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Windy", "Foggy"]
    city_hash = abs(hash(city.lower()))
    return conditions[city_hash % len(conditions)]


class InteractionHistory:
    """Stores a sequential history of actions taken and their results."""

    def __init__(self):
        # Use the clear field name 'interactions' holding a list of ActionOutcome
        self.interactions: List[Interaction] = []

    def add_interaction(self, action: Any, result: Any):
        """Adds a new action and its result to the history."""
        outcome = Interaction(action=action, result=result)
        self.interactions.append(outcome)

    def get_last_interaction(self) -> Interaction | None:
        """Returns the most recent interaction, or None if history is empty."""
        if not self.interactions:
            return None
        return self.interactions[-1]

    def __len__(self) -> int:
        """Returns the number of interactions recorded."""
        return len(self.interactions)
