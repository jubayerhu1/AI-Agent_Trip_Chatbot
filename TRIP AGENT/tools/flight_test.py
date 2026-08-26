import os 
import re 
import certifi
import airportsdata
import pycountry
import requests
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()



# ==========================================
# Aviationstack Flight Information
# ==========================================

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


def get_flight_info(flight_number):
    """
    Get flight information from Aviationstack API.

    Example:
        get_flight_info("EK215")
    """

    url = "https://api.aviationstack.com/v1/flights"
    #BASE_URL = "https://api.aviationstack.com/v1/flights"


    params = {
        "access_key": API_KEY,
        "flight_iata": flight_number
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        # Check HTTP response
        response.raise_for_status()

        data = response.json()

        # Check Aviationstack API error
        if "error" in data:
            print("API Error:")
            print(data["error"])
            return None

        flights = data.get("data", [])

        if not flights:
            print("No flight information found.")
            return None

        return flights[0]

    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return None


# ==========================================
# Get Flight Information
# ==========================================

flight = get_flight_info("EK215")


# ==========================================
# Display Flight Information
# ==========================================

if flight:

    print("\n========== FLIGHT INFORMATION ==========")

    print("Airline       :", flight.get("airline", {}).get("name"))
    print("Flight Number :", flight.get("flight", {}).get("iata"))
    print("Flight Status :", flight.get("flight_status"))

    print("\n---------- DEPARTURE ----------")

    departure = flight.get("departure", {})

    print("Airport       :", departure.get("airport"))
    print("IATA          :", departure.get("iata"))
    print("Terminal      :", departure.get("terminal"))
    print("Gate          :", departure.get("gate"))
    print("Scheduled     :", departure.get("scheduled"))
    print("Estimated     :", departure.get("estimated"))

    print("\n---------- ARRIVAL ----------")

    arrival = flight.get("arrival", {})

    print("Airport       :", arrival.get("airport"))
    print("IATA          :", arrival.get("iata"))
    print("Terminal      :", arrival.get("terminal"))
    print("Gate          :", arrival.get("gate"))
    print("Scheduled     :", arrival.get("scheduled"))
    print("Estimated     :", arrival.get("estimated"))

    print("\n========================================")