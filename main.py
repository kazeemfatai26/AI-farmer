from farmer import get_farmer
from weather import get_weather
from recommendation import get_recommendation
from translator import generate_advisory
from sms import send_sms


def main():

    # ==================================
    # Farmer ID
    # ==================================

    farmer_id = "6a7b340c07760aace3f29d9b"


    # ==================================
    # 1. Fetch farmer
    # ==================================

    print("Fetching farmer information...")

    farmer = get_farmer(farmer_id)

    print(f"Farmer: {farmer['name']}")
    print(f"Crop: {farmer['crop_type']}")
    print(f"Phone: {farmer['phone_number']}")


    # ==================================
    # 2. Fetch weather
    # ==================================

    location = (
        f"{farmer['sector']}, "
        f"{farmer['district']}, Rwanda"
    )

    print("\nFetching weather...")

    weather = get_weather(location)

    print("Weather received.")

    print(
        f"Temperature: "
        f"{weather['current']['temperature']} °C"
    )

    print(
        f"Condition: "
        f"{weather['current']['weather_descriptions'][0]}"
    )


    # ==================================
    # 3. Fetch ML recommendation
    # ==================================

    print("\nFetching ML recommendation...")

    recommendation = get_recommendation(
        farmer_id
    )

    print("Recommendation received.")

    print(
        "Prediction:",
        recommendation["prediction"]
    )


    # ==================================
    # 4. Generate advisory with Gemini
    # ==================================

    print("\nGenerating advisory...")

    message = generate_advisory(
        farmer,
        weather,
        recommendation
    )

    print("\nGenerated SMS:")
    print("-----------------------------")
    print(message)
    print("-----------------------------")


    # ==================================
    # 5. Send SMS
    # ==================================

    print("\nSending SMS...")

    print(
        f"Recipient phone number: "
        f"{farmer['phone_number']}"
    )

    response = send_sms(
        farmer["phone_number"],
        message
    )

    print("\nSMS response:")
    print(response)


# ==================================
# Run program
# ==================================

if __name__ == "__main__":
    main()