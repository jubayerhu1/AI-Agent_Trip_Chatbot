import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_flights(query:str, int =5):
    """
    Search flights using Aviationstack API.

    Example:
        search_flights("JFK")
        search_flights("LAX")
    """

    API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

    if not API_KEY:
        raise ValueError("AVIATIONSTACK_API_KEY is not set")

    url = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "dep_iata": query
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"API request failed: {response.status_code} - {response.text}"
        )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    return data




result = search_flights("7 days plan USA to BD")

print(result)



