from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def translate_to_kinyarwanda(weather):

    location = weather["location"]["name"]
    temperature = weather["current"]["temperature"]
    feels_like = weather["current"]["feelslike"]
    condition = weather["current"]["weather_descriptions"][0]
    rainfall = weather["current"]["precip"]
    humidity = weather["current"]["humidity"]
    wind_speed = weather["current"]["wind_speed"]
    cloud_cover = weather["current"]["cloudcover"]

    weather_info = f"""
Location: {location}
Temperature: {temperature} °C
Feels like: {feels_like} °C
Condition: {condition}
Rainfall: {rainfall} mm
Humidity: {humidity} %
Wind speed: {wind_speed} km/h
Cloud cover: {cloud_cover} %
"""

    prompt = f"""
You are an agricultural advisory assistant for
smallholder farmers in Rwanda.

Weather information:
{weather_info}

Create a short agricultural advisory.

Return EXACTLY this format:

KINYARWANDA:
[Simple Kinyarwanda SMS]

ENGLISH:
[English translation]

Requirements:
- Use simple Kinyarwanda.
- Make it understandable to a rural farmer.
- Include useful measurements such as temperature,
  rainfall, and humidity.
- Give practical agricultural advice based ONLY on
  the weather information provided.
- Do not invent information.
- Keep each message short enough for SMS.
- Do not use technical language.
- Do not use emojis.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()