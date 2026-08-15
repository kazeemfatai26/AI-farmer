import requests
from config import RECOMMENDATION_API_URL


def get_recommendation(farmer_id):

    url = f"{RECOMMENDATION_API_URL}/{farmer_id}"

    print(f"Requesting recommendation from: {url}")

    response = requests.get(
        url,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):

        if not data:
            raise ValueError(
                "No recommendation found"
            )

        data = data[0]

    if data.get("status") != "success":
        raise ValueError(
            "Recommendation API failed"
        )

    return data