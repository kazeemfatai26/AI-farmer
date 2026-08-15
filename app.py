from fastapi import FastAPI, HTTPException

from farmer import get_farmer
from weather import get_weather
from recommendation import get_recommendation
from translator import generate_advisory
from sms import send_sms


app = FastAPI(
    title="AI Farmer Advisory API",
    description="Agricultural advisory and SMS service",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "status": "running",
        "service": "AI Farmer Advisory API"
    }


@app.post("/send-advisory/{farmer_id}")
def send_advisory(farmer_id: str):

    try:

        # ==========================
        # 1. Get farmer
        # ==========================

        farmer = get_farmer(farmer_id)


        # ==========================
        # 2. Get weather
        # ==========================

        location = (
            f"{farmer['sector']}, "
            f"{farmer['district']}, Rwanda"
        )

        weather = get_weather(location)


        # ==========================
        # 3. Get ML recommendation
        # ==========================

        recommendation = get_recommendation(
            farmer_id
        )


        # ==========================
        # 4. Generate SMS
        # ==========================

        message = generate_advisory(
            farmer,
            weather,
            recommendation
        )


        # ==========================
        # 5. Send SMS
        # ==========================

        sms_response = send_sms(
            farmer["phone_number"],
            message
        )


        return {
            "status": "success",
            "farmer": {
                "id": farmer["_id"],
                "name": farmer["name"],
                "phone": farmer["phone_number"],
                "crop": farmer["crop_type"]
            },
            "weather": {
                "temperature": weather["current"]["temperature"],
                "condition": weather["current"]["weather_descriptions"][0],
                "rainfall": weather["current"]["precip"],
                "humidity": weather["current"]["humidity"]
            },
            "recommendation": recommendation["prediction"],
            "message": message,
            "sms_response": sms_response
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )