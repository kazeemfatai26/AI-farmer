import requests
from config import FARMER_API_URL


def get_farmer(farmer_id):

    url = f"{FARMER_API_URL}/fetchFarmer/{farmer_id}"

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):

        if not data:
            raise ValueError("Farmer not found")

        return data[0]

    if isinstance(data, dict):

        if "_id" in data:
            return data

        if "data" in data:
            farmer = data["data"]

            if isinstance(farmer, list):
                return farmer[0]

            return farmer

    raise ValueError("Unexpected farmer API response")