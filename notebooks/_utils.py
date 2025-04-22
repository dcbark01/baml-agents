import re


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
