from smsmobileapi import SMSSender
from config import SMS_API_KEY


def send_sms(phone_number, message):

    # ==================================
    # Display recipient
    # ==================================

    print(f"SMS recipient: {phone_number}")


    # ==================================
    # Create SMS sender
    # ==================================

    sms = SMSSender(
        api_key=SMS_API_KEY
    )


    # ==================================
    # Send SMS
    # ==================================

    response = sms.send_message(
        to=phone_number,
        message=message
    )


    # ==================================
    # Return response
    # ==================================

    return response