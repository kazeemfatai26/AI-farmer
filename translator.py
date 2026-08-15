from google import genai
from google.genai.errors import ClientError

from config import GEMINI_API_KEY, GEMINI_MODEL


# =========================================================
# Gemini client
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# Generate agricultural advisory
# =========================================================

def generate_advisory(
    farmer,
    weather,
    recommendation
):

    current = weather["current"]

    # -----------------------------------------------------
    # Weather information
    # -----------------------------------------------------

    temperature = current.get("temperature", "N/A")

    condition = current.get(
        "weather_descriptions",
        ["N/A"]
    )[0]

    rainfall = current.get(
        "precip",
        "N/A"
    )

    humidity = current.get(
        "humidity",
        "N/A"
    )

    wind_speed = current.get(
        "wind_speed",
        "N/A"
    )


    # -----------------------------------------------------
    # ML recommendation
    # -----------------------------------------------------

    prediction = recommendation.get(
        "prediction",
        {}
    )

    fertilizer_rate = prediction.get(
        "fertilizer_rate",
        0
    )

    inorganic_fertilizer_rate = prediction.get(
        "inorganic_fertilizer_rate",
        0
    )

    irrigation_rate = prediction.get(
        "irrigation_rate",
        0
    )

    pesticide_rate = prediction.get(
        "pesticide_rate",
        0
    )


    # -----------------------------------------------------
    # Farmer information
    # -----------------------------------------------------

    name = farmer.get(
        "name",
        "Mworozi"
    )

    crop = farmer.get(
        "crop_type",
        "igihingwa"
    )

    district = farmer.get(
        "district",
        ""
    )

    sector = farmer.get(
        "sector",
        ""
    )


    # =====================================================
    # Gemini prompt
    # =====================================================

    prompt = f"""
You are an agricultural advisory assistant helping
smallholder farmers in Rwanda.

Generate a short SMS in very simple Kinyarwanda.

Farmer:
Name: {name}
Crop: {crop}
District: {district}
Sector: {sector}

Weather:
Temperature: {temperature} °C
Condition: {condition}
Rainfall: {rainfall} mm
Humidity: {humidity}%
Wind speed: {wind_speed} km/h

Machine learning recommendation:
Fertilizer rate: {fertilizer_rate}
Inorganic fertilizer rate: {inorganic_fertilizer_rate}
Irrigation rate: {irrigation_rate}
Pesticide rate: {pesticide_rate}

Requirements:

- Use simple Kinyarwanda that a rural farmer can understand.
- Include the weather information.
- Include temperature and rainfall.
- Include the fertilizer recommendation.
- Include irrigation recommendation.
- Include pesticide recommendation.
- Give practical advice.
- Keep the SMS short.
- Do not invent information.
- Preserve all important numbers.
- Return ONLY the SMS.
"""


    # =====================================================
    # TRY GEMINI
    # =====================================================

    try:

        print("Calling Gemini...")

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        message = response.text.strip()

        print("Gemini advisory generated successfully.")

        return {
            "message": message,
            "ai_generated": True,
            "source": "Gemini"
        }


    # =====================================================
    # GEMINI QUOTA ERROR
    # =====================================================

    except ClientError as e:

        print("Gemini ClientError:")
        print(e)


        if e.code == 429:

            print(
                "Gemini quota exceeded."
            )

            print(
                "Using fallback agricultural advisory."
            )


            # ------------------------------------------------
            # FALLBACK SMS
            # ------------------------------------------------

            fallback_message = (
                f"Muraho {name}. "
                f"Ikirere muri {sector}: {condition}, "
                f"ubushyuhe ni {temperature}°C, "
                f"imvura ni {rainfall}mm, "
                f"ubukonje bw'ikirere ni {humidity}%. "
                f"Ku bihingwa bya {crop}: "
                f"fumbire yasabwe ni {fertilizer_rate}, "
                f"kuhira ni {irrigation_rate}, "
                f"n'imiti yica udukoko ni {pesticide_rate}."
            )


            return {
                "message": fallback_message,
                "ai_generated": False,
                "source": "Fallback"
            }


        # ------------------------------------------------
        # Other Gemini errors
        # ------------------------------------------------

        print(
            "Gemini failed for another reason."
        )

        fallback_message = (
            f"Muraho {name}. "
            f"Ikirere: {condition}. "
            f"Ubushyuhe: {temperature}°C. "
            f"Imvura: {rainfall}mm. "
            f"Ubushuhe: {humidity}%. "
            f"Ku bihingwa bya {crop}, "
            f"fumbire yasabwe: {fertilizer_rate}. "
            f"Kuhira: {irrigation_rate}. "
            f"Imiti yica udukoko: {pesticide_rate}."
        )

        return {
            "message": fallback_message,
            "ai_generated": False,
            "source": "Fallback"
        }


    # =====================================================
    # UNEXPECTED ERROR
    # =====================================================

    except Exception as e:

        print(
            "Unexpected Gemini error:"
        )

        print(e)


        fallback_message = (
            f"Muraho {name}. "
            f"Ikirere: {condition}, "
            f"ubushyuhe {temperature}°C, "
            f"imvura {rainfall}mm. "
            f"Ku bihingwa bya {crop}, "
            f"fumbire: {fertilizer_rate}, "
            f"kuhira: {irrigation_rate}, "
            f"imiti yica udukoko: {pesticide_rate}."
        )


        return {
            "message": fallback_message,
            "ai_generated": False,
            "source": "Fallback"
        }