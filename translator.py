from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_advisory(
    farmer,
    weather,
    recommendation
):

    # Farmer information
    name = farmer["name"]
    district = farmer["district"]
    sector = farmer["sector"]
    crop = farmer["crop_type"]
    planting_date = farmer["planting_date"]

    # Weather information
    current = weather["current"]

    temperature = current["temperature"]
    feels_like = current["feelslike"]
    condition = current["weather_descriptions"][0]
    rainfall = current["precip"]
    humidity = current["humidity"]
    wind_speed = current["wind_speed"]
    wind_direction = current["wind_dir"]

    # ML recommendation
    prediction = recommendation["prediction"]

    fertilizer_rate = prediction["fertilizer_rate"]
    inorganic_fertilizer_rate = (
        prediction["inorganic_fertilizer_rate"]
    )
    irrigation_rate = prediction["irrigation_rate"]
    pesticide_rate = prediction["pesticide_rate"]
    harvest = prediction["median_harvest_kg"]

    prompt = f"""
You are an agricultural advisory assistant
for smallholder farmers in Rwanda.

FARMER:
Name: {name}
District: {district}
Sector: {sector}
Crop: {crop}
Planting date: {planting_date}

WEATHER:
Temperature: {temperature} °C
Feels like: {feels_like} °C
Condition: {condition}
Rainfall: {rainfall} mm
Humidity: {humidity} %
Wind speed: {wind_speed} km/h
Wind direction: {wind_direction}

ML RECOMMENDATION:
Fertilizer rate: {fertilizer_rate}
Inorganic fertilizer rate: {inorganic_fertilizer_rate}
Irrigation rate: {irrigation_rate}
Pesticide rate: {pesticide_rate}
Median expected harvest: {harvest} kg

Create a short agricultural advisory SMS.

Return exactly:

KINYARWANDA:
[message]

ENGLISH:
[message]

Rules:
- Use simple Kinyarwanda.
- Make the message easy for rural farmers.
- Include useful weather measurements.
- Include the crop when relevant.
- Use the ML recommendation.
- Do not invent values.
- Do not change numerical values.
- If a recommendation is 0, do not tell the farmer
  to apply that input.
- Keep both messages short.
- Do not use emojis.
- Return only the two messages.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()