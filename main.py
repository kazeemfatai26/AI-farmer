from weather import get_weather
from translator import translate_to_kinyarwanda
from sms import send_sms


def main():



    location = "Nyagatare, Rwanda"

    phone_number = "+250790466267"



    print("Getting weather...")

    weather = get_weather(location)

    print("Weather received.")


    print("Generating Kinyarwanda advisory...")

    message = translate_to_kinyarwanda(weather)

    print("\nSMS message:")
    print(message)

    print("\nSending SMS...")

    response = send_sms(
        phone_number,
        message
    )

    print("SMS response:")
    print(response)


if __name__ == "__main__":
    main()