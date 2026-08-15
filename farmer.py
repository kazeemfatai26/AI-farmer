import requests
from config import FARMER_API_URL


def get_farmer(farmer_id):

    url = f"{FARMER_API_URL}/fetchFarmer/{farmer_id}"

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    print("Farmer API response:", data)

    # If API returns a list
    if isinstance(data, list):

        if not data:
            raise ValueError("Farmer not found")

        return data[0]

    # If API returns a dictionary
    elif isinstance(data, dict):

        # Direct farmer object
        if "_id" in data:
            return data

        # If farmer is nested inside a key
        if "data" in data:
            farmer_data = data["data"]

            if isinstance(farmer_data, list):
                return farmer_data[0]

            return farmer_data

    raise ValueError("Unexpected farmer API response format")