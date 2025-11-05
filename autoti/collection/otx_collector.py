# This script is responsible for collecting threat intelligence data from AlienVault OTX (Open Threat Exchange).
# It fetches recent 'pulses', which are collections of threat indicators.

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from a '.env' file for secure handling of API keys.
load_dotenv()

# --- API CONFIGURATION ---
# Retrieve the OTX API key from environment variables.
# Using .get() provides a default value to avoid errors if the key is not set.
OTX_API_KEY = os.environ.get("OTX_API_KEY", "YOUR_API_KEY_HERE")
# The base URL for the AlienVault OTX API.
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
    if api_key in ("YOUR_API_KEY_HERE", None):
        print("ERROR: OTX API Key is missing. Please set it in your .env file.")
        return []

    # The API requires the key to be sent in the request headers.
    headers = {
        "X-OTX-API-KEY": api_key
    }

    # To get the most recent data, we calculate the timestamp for 24 hours ago.
    # The API will return pulses modified since this time.
    since_timestamp = (datetime.now() - timedelta(days=1)).isoformat()

    # Construct the full URL for the API endpoint.
    # We are querying the 'subscribed' pulses endpoint.
    url = f"{BASE_URL}/pulses/subscribed?modified_since={since_timestamp}"

    try:
        # Make the GET request to the OTX API.
        response = requests.get(url, headers=headers, timeout=15) # Adding a timeout is good practice.
        # This will raise an exception if the response has a bad status code (like 404 or 500).
        response.raise_for_status()

        # Parse the JSON response from the API.
        data = response.json()
        print(f"Successfully fetched {len(data.get('results', []))} pulses from AlienVault OTX.")
        # The actual pulse data is in the 'results' key of the response.
        return data.get("results", [])

    # --- ROBUST ERROR HANDLING ---
    # It's important to handle different types of potential errors when making API calls.
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response. The API might be down or returning invalid data.")

    # Return an empty list if any error occurred.
    return []

# --- STANDALONE EXECUTION FOR TESTING ---
if __name__ == "__main__":
    # This block allows the script to be run directly for testing purposes.
    # For example, you can run 'python autoti/collection/otx_collector.py' from the root directory.
    print("--- Testing OTX Data Collector ---")
    latest_pulses = get_latest_pulses(OTX_API_KEY)

    if latest_pulses:
        print(f"\nSuccessfully fetched {len(latest_pulses)} pulses.")
        # Print details of the first 2 pulses for a quick review.
        for pulse in latest_pulses[:2]:
            print("\n--- Sample Pulse ---")
            print(f"  Name: {pulse.get('name')}")
            print(f"  Created: {pulse.get('created')}")
            print(f"  Description: {pulse.get('description', 'No description available.')[:100]}...")
            print(f"  IOC Count: {len(pulse.get('indicators', []))}")
    else:
        print("\nNo pulses fetched. Please check your API key and network connection.")
