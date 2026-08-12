import os
from dotenv import load_dotenv

load_dotenv()

# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SMS_API_KEY = os.getenv("SMS_API_KEY")

# Gemini model
GEMINI_MODEL = "gemini-3.5-flash"


# Check required API keys
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is missing from .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

if not SMS_API_KEY:
    raise ValueError("SMS_API_KEY is missing from .env")