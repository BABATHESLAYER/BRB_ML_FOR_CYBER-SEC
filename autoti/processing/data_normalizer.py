import pandas as pd
from datetime import datetime

def normalize_pulses(raw_pulses):
    """
    Normalizes a list of raw threat intelligence pulses into a structured pandas DataFrame.

    Args:
        raw_pulses (list): A list of dictionaries, where each dictionary is a raw pulse from OTX.

    Returns:
        pandas.DataFrame: A DataFrame containing the normalized threat intelligence data.
                          Returns an empty DataFrame if the input is empty.
    """
    if not raw_pulses:
        print("Input pulse list is empty. Returning an empty DataFrame.")
        return pd.DataFrame()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(raw_pulses)

    # --- Data Cleaning and Structuring ---

    # 1. Select relevant columns. We can expand this list as needed.
    # We are interested in the pulse's name, description, creation date, and associated indicators.
    required_columns = ['id', 'name', 'description', 'created', 'indicators']

    # Filter for columns that exist in the DataFrame to avoid errors
    existing_columns = [col for col in required_columns if col in df.columns]
    df_normalized = df[existing_columns].copy()

    # 2. Rename columns for clarity and consistency
    rename_map = {
        'id': 'pulse_id',
        'name': 'threat_name',
        'description': 'threat_description',
        'created': 'creation_date'
    }
    df_normalized.rename(columns=rename_map, inplace=True)

    # 3. Handle missing or null values
    df_normalized['threat_description'].fillna('No description provided.', inplace=True)

    # 4. Convert data types for consistency
    # Convert 'creation_date' from string to datetime objects
    df_normalized['creation_date'] = pd.to_datetime(df_normalized['creation_date'])

    # 5. Extract and count IOCs (Indicators of Compromise)
    # This creates a new column with the number of IOCs for each pulse
    if 'indicators' in df_normalized.columns:
        df_normalized['ioc_count'] = df_normalized['indicators'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    else:
        df_normalized['ioc_count'] = 0


    print("Data normalization complete.")
    return df_normalized

if __name__ == "__main__":
    # --- Sample Raw Data (for testing) ---
    # This simulates the kind of data we would get from otx_collector.py
    sample_raw_data = [
        {
            "id": "668ba07c0823521f753c8c87",
            "name": "Malicious IPs related to Phishing Campaign",
            "description": "A new set of IPs hosting phishing sites targeting financial institutions.",
            "created": "2025-11-03T10:00:00.000Z",
            "indicators": [
                {"type": "IPv4", "indicator": "198.51.100.1"},
                {"type": "IPv4", "indicator": "198.51.100.2"}
            ]
        },
        {
            "id": "668ba07c0823521f753c8c88",
            "name": "Fake Browser Update (SocGholish)",
            "description": "", # Simulating a missing description
            "created": "2025-11-03T11:30:00.000Z",
            "indicators": [
                {"type": "URL", "indicator": "http://evil-site.com/update.js"}
            ]
        }
    ]

    print("--- Running Data Normalizer with Sample Data ---")
    normalized_df = normalize_pulses(sample_raw_data)

    # Print the resulting DataFrame to verify
    print("\n--- Normalized DataFrame ---")
    print(normalized_df.head())
    print("\n--- DataFrame Info ---")
    normalized_df.info()
