import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Your AlienVault OTX API Key.
# It's recommended to use an environment variable for security.
OTX_API_KEY = os.environ.get("OTX_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://otx.alienvault.com/api/v1"


def get_latest_pulses(api_key):
    """
    Fetches the latest threat intelligence pulses from AlienVault OTX from the last 24 hours.

    Args:
        api_key (str): Your AlienVault OTX API key.

    Returns:
        list: A list of dictionaries, where each dictionary is a threat pulse.
              Returns an empty list if the request fails.
    """
    if api_key == "YOUR_API_KEY_HERE":
        print("ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual AlienVault OTX API key.")
        return []

    headers = {
        "X-OTX-API-KEY": api_key
    }

    # Get the timestamp for 24 hours ago
    since_timestamp = (datetime.now() - timedelta(days=1)).isoformat()

    # The endpoint to get pulses created in the last 24 hours
    url = f"{BASE_URL}/pulses/subscribed?modified_since={since_timestamp}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        print(f"Successfully fetched {len(data.get('results', []))} pulses from AlienVault OTX.")
        return data.get("results", [])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")

    return []

if __name__ == "__main__":
    print("Fetching latest threat intelligence pulses from AlienVault OTX...")
    latest_pulses = get_latest_pulses(OTX_API_KEY)

    if latest_pulses:
        # Print details of the first 5 pulses for a quick review
        for pulse in latest_pulses[:5]:
            print("\n--- Pulse ---")
            print(f"Name: {pulse.get('name')}")
            print(f"Created: {pulse.get('created')}")
            print(f"Description: {pulse.get('description', 'No description available.')}")
            # To see all indicators of compromise (IOCs)
            # print(f"Indicators: {pulse.get('indicators')}")
    else:
        print("No pulses fetched. Please check your API key and network connection.")
