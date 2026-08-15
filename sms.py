import requests
from config import SMS_API_KEY


def send_sms(phone_number, message):

    print(f"SMS recipient: {phone_number}")

    # Check API key
    if not SMS_API_KEY:
        raise ValueError(
            "SMS_API_KEY is missing from environment variables"
        )

    print("SMS API key is loaded")
    print(f"API key length: {len(SMS_API_KEY)}")

    # SMS Mobile API endpoint
    url = "https://api.smsmobileapi.com/sendsms/"

    # IMPORTANT:
    # SMS Mobile API expects "apikey" and "recipients"
    payload = {
        "recipients": phone_number,
        "message": message,
        "apikey": SMS_API_KEY
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    print("SMS HTTP status:", response.status_code)
    print("SMS API response:", response.text)

    response.raise_for_status()

    try:
        result = response.json()
    except ValueError:
        return response.text

    return result