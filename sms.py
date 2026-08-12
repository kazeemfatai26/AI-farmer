from smsmobileapi import SMSSender
from config import SMS_API_KEY


def send_sms(phone_number, message):

    sms = SMSSender(
        api_key=SMS_API_KEY
    )

    response = sms.send_message(
        to=phone_number,
        message=message
    )

    return response
