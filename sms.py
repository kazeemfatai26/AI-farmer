import requests
from config import SMS_API_KEY


def send_sms(phone_number, message):

    print(f"SMS recipient: {phone_number}")

    url = "https://api.smsmobileapi.com/sendsms"

    payload = {
        "api_key": SMS_API_KEY,
        "to": phone_number,
        "message": message
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    print("SMS status:", response.status_code)
    print("SMS response:", response.text)

    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return response.text