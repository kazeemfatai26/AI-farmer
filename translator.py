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
Translate into Kinyarwanda in simple farmer language. 
    Keep it short and practical. 
    Explain the recommendations using words like low, moderate, high, suitable, and needs attention. 
    Include raw numbers and the recommendation alongside it.

Message: Hi {name}, your crop is {crop}, and you are in {district}, {sector}. We compared your farm with similar farms in your area. 
The recommendation suggests a suitable level of fertilizer, irrigation, and pest control for your crop and season.
Today’s weather is {condition}, with {temperature} °C, {rainfall} mm rainfall, {humidity}% humidity, and {wind_speed} km/h wind speed.
This weather affects crop growth, water needs, and pest pressure. 
We recommend using the right fertilizer, giving enough water, protecting the crop from pests, and checking the field regularly. 
This advice is based on similar farms and is meant to help you improve your harvest.

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
                f"""Muraho {name}. "
f"Murakoze kubaha amakuru. Ibi birimo gutunganywa mu buryo bw’inyuma, kandi turacyakora kugira ngo tubagezeho ibisubizo by’ukurima kwawe. 
Niba utabasha kubona ibisubizo vuba, nyamuneka uhore wihanganiye, turagusubiza muri make.
Turabashimiye kubumvaga, kandi turacyakora kugira ngo tugufashe mu gihe gito."""
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
f"""Murakoze kubaha amakuru. Ibi birimo gutunganywa mu buryo bw’inyuma, kandi turacyakora kugira ngo tubagezeho ibisubizo by’ukurima kwawe. 
Niba utabasha kubona ibisubizo vuba, nyamuneka uhore wihanganiye, turagusubiza muri make.
Turabashimiye kubumvaga, kandi turacyakora kugira ngo tugufashe mu gihe gito."""
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
f"""Murakoze kubaha amakuru. Ibi birimo gutunganywa mu buryo bw’inyuma, kandi turacyakora kugira ngo tubagezeho ibisubizo by’ukurima kwawe. 
Niba utabasha kubona ibisubizo vuba, nyamuneka uhore wihanganiye, turagusubiza muri make.
Turabashimiye kubumvaga, kandi turacyakora kugira ngo tugufashe mu gihe gito."""
        )


        return {
            "message": fallback_message,
            "ai_generated": False,
            "source": "Fallback"
        }
