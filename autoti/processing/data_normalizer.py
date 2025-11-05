# This script is responsible for cleaning and structuring the raw data collected from OTX.
# Data normalization is a critical step to ensure the data is consistent and easy to work with
# in the analysis phase. We use the pandas library for efficient data manipulation.

import pandas as pd

def normalize_pulses(raw_pulses):
    """
    Normalizes a list of raw threat intelligence pulses into a structured pandas DataFrame.

    The process involves:
    - Selecting relevant columns.
    - Renaming columns for clarity.
    - Handling missing data.
    - Converting data types.
    - Extracting and creating new, useful features (like IOC count).

    Args:
        raw_pulses (list): A list of dictionaries, where each is a raw pulse from OTX.

    Returns:
        pandas.DataFrame: A clean, structured DataFrame. Returns an empty DataFrame on failure.
    """
    if not raw_pulses:
        print("Input pulse list is empty. Returning an empty DataFrame.")
        return pd.DataFrame()

    # Convert the list of dictionaries into a pandas DataFrame for easier processing.
    df = pd.DataFrame(raw_pulses)

    # --- Data Cleaning and Structuring ---

    # 1. Select Relevant Columns
    # We choose the columns that are most useful for our analysis.
    required_columns = ['id', 'name', 'description', 'created', 'indicators']

    # We filter for columns that actually exist in the DataFrame to avoid errors
    # if the API response changes.
    existing_columns = [col for col in required_columns if col in df.columns]
    df_normalized = df[existing_columns].copy()

    # 2. Rename Columns
    # We use more descriptive and consistent column names.
    rename_map = {
        'id': 'pulse_id',
        'name': 'threat_name',
        'description': 'threat_description',
        'created': 'creation_date'
    }
    df_normalized.rename(columns=rename_map, inplace=True)

    # 3. Handle Missing Values
    # We replace any empty 'description' fields with a standard placeholder.
    df_normalized['threat_description'].fillna('No description provided.', inplace=True)

    # 4. Convert Data Types
    # The 'created' field is a string, but it's more useful as a datetime object
    # for any time-based analysis.
    df_normalized['creation_date'] = pd.to_datetime(df_normalized['creation_date'])

    # 5. Feature Engineering: Extract and Count IOCs
    # We create a new column, 'ioc_count', to store the number of Indicators of Compromise
    # for each threat pulse. This is a useful metric for assessing the pulse's scope.
    if 'indicators' in df_normalized.columns:
        df_normalized['ioc_count'] = df_normalized['indicators'].apply(lambda ioc_list: len(ioc_list) if isinstance(ioc_list, list) else 0)
    else:
        df_normalized['ioc_count'] = 0

    print("Data normalization complete.")
    return df_normalized

# --- STANDALONE EXECUTION FOR TESTING ---
if __name__ == "__main__":
    # This block allows the script to be run directly for testing.
    # We use sample data that mimics the structure of the real API response.
    print("--- Testing Data Normalizer with Sample Data ---")

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
            "description": "", # Simulate a missing description.
            "created": "2025-11-03T11:30:00.000Z",
            "indicators": [
                {"type": "URL", "indicator": "http://evil-site.com/update.js"}
            ]
        }
    ]

    normalized_df = normalize_pulses(sample_raw_data)

    # Print the resulting DataFrame to verify the normalization process.
    print("\n--- Normalized DataFrame ---")
    print(normalized_df.head())
    print("\n--- DataFrame Info ---")
    # .info() gives a useful summary of the DataFrame's structure and data types.
    normalized_df.info()
