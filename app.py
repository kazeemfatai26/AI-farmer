from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback

from farmer import get_farmer
from weather import get_weather
from recommendation import get_recommendation
from translator import generate_advisory
from sms import send_sms


# Create FastAPI application


app = FastAPI(
    title="AI Farmer Advisory API",
    description="Agricultural advisory and SMS service",
    version="1.0.0"
)


# CORS


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint


@app.get("/")
def home():

    return {
        "status": "running",
        "service": "AI Farmer Advisory API",
        "message": "API is working successfully"
    }


# Health check


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# Send agricultural advisory


@app.post("/send-advisory/{farmer_id}")
def send_advisory(farmer_id: str):

    try:

        print("\n========================================")
        print("STARTING FARMER ADVISORY")
        print("========================================")

        print(f"Farmer ID: {farmer_id}")


   
        # 1. FETCH FARMER
       

        print("\n[1/5] Fetching farmer information...")

        farmer = get_farmer(farmer_id)

        print("Farmer information received.")
        print(f"Farmer name: {farmer['name']}")
        print(f"Phone: {farmer['phone_number']}")
        print(f"District: {farmer['district']}")
        print(f"Sector: {farmer['sector']}")
        print(f"Crop: {farmer['crop_type']}")


        # 2. FETCH WEATHER
        

        location = (
            f"{farmer['sector']}, "
            f"{farmer['district']}, "
            f"Rwanda"
        )

        print("\n[2/5] Fetching weather...")
        print(f"Weather location: {location}")

        weather = get_weather(location)

        current_weather = weather["current"]

        temperature = current_weather["temperature"]

        condition = current_weather[
            "weather_descriptions"
        ][0]

        rainfall = current_weather["precip"]

        humidity = current_weather["humidity"]

        wind_speed = current_weather["wind_speed"]

        cloudcover = current_weather["cloudcover"]

        print("Weather received.")
        print(f"Temperature: {temperature} °C")
        print(f"Condition: {condition}")
        print(f"Rainfall: {rainfall} mm")
        print(f"Humidity: {humidity}%")
        print(f"Wind speed: {wind_speed} km/h")
        print(f"Cloud cover: {cloudcover}%")


     
        # 3. FETCH ML RECOMMENDATION
      

        print("\n[3/5] Fetching ML recommendation...")

        recommendation = get_recommendation(
            farmer_id
        )

        print("Recommendation received.")
        print(recommendation)

        # 4. GENERATE SMS WITH GEMINI
    

        print("\n[4/5] Generating agricultural advisory...")

        message = generate_advisory(
            farmer,
            weather,
            recommendation
        )

        print("Advisory generated successfully.")

        print("\nGenerated SMS:")
        print("----------------------------------------")
        print(message)
        print("----------------------------------------")


      
        # 5. SEND SMS
      

        print("\n[5/5] Sending SMS...")

        sms_response = send_sms(
            farmer["phone_number"],
            message
        )

        print("SMS sent successfully.")
        print("SMS response:", sms_response)


        # RETURN RESULT
       

        print("\n========================================")
        print("ADVISORY COMPLETED SUCCESSFULLY")
        print("========================================")

        return {

            "status": "success",

            "farmer": {
                "id": farmer["_id"],
                "name": farmer["name"],
                "phone": farmer["phone_number"],
                "district": farmer["district"],
                "sector": farmer["sector"],
                "crop": farmer["crop_type"],
                "preferred_language": farmer.get(
                    "preferred_language"
                )
            },

            "weather": {
                "location": location,
                "temperature": temperature,
                "condition": condition,
                "rainfall_mm": rainfall,
                "humidity_percent": humidity,
                "wind_speed_kmh": wind_speed,
                "cloud_cover_percent": cloudcover
            },

            "recommendation": recommendation.get(
                "prediction",
                {}
            ),

            "message": message,

            "sms_response": sms_response
        }


    # ERROR HANDLING
  

    except Exception as e:

        print("\n========================================")
        print("ERROR IN FARMER ADVISORY")
        print("========================================")

        print(f"Error: {str(e)}")

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e),
                "farmer_id": farmer_id
            }
        )