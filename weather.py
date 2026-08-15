import requests
from config import WEATHER_API_KEY


def get_weather(location):

    url = "https://api.weatherstack.com/current"

    params = {
        "access_key": WEATHER_API_KEY,
        "query": location
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise ValueError(
            data["error"].get(
                "info",
                "Weather API error"
            )
        )

    return data