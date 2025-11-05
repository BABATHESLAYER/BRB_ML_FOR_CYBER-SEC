# import os
# import sys
# import pandas as pd
# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# from langchain_classic.chains import LLMChain
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Load environment variables from .env file
# load_dotenv()

# # Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# # Import the data collection and normalization functions
# from autoti.collection.otx_collector import get_latest_pulses, OTX_API_KEY
# from autoti.processing.data_normalizer import normalize_pulses

# # --- Configuration ---
# # Your Google API Key.
# # It's recommended to use an environment variable for security.
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")

# def get_llm(api_key):
#     """Initializes and returns the ChatGoogleGenerativeAI model."""
#     if api_key == "YOUR_API_KEY_HERE":
#         print("ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual Google API key.")
#         return None

#     # Initialize the LLM - we'll use Google's gemini-pro as a default
#     return ChatGoogleGenerativeAI(
#         google_api_key=api_key,
#         model="gemini-2.5-flash",
#         temperature=0.2,
#         convert_system_message_to_human=True # Gemini uses a different prompting strategy
#     )

# def generate_threat_report(normalized_data, llm):
#     """
#     Generates a concise threat intelligence report using LangChain and an LLM.

#     Args:
#         normalized_data (pd.DataFrame): A DataFrame with normalized threat data.
#         llm (ChatGoogleGenerativeAI): The initialized LangChain LLM.

#     Returns:
#         str: The generated threat intelligence report.
#              Returns an error message if report generation fails.
#     """
#     if llm is None:
#         return "Report generation failed due to missing LLM configuration."

#     if normalized_data.empty:
#         return "No threat data available to generate a report."

#     # Convert the DataFrame to a string format that's easy for the LLM to parse.
#     # We'll use a summary of the top threats.
#     top_threats = normalized_data.head(5)
#     data_summary_str = top_threats.to_string(
#         columns=['threat_name', 'threat_description', 'ioc_count'],
#         index=False
#     )

#     # --- Prompt Engineering ---
#     # This is the core of the agent's logic. We instruct the LLM on its role,
#     # the format of the output, and what data to use.
#     prompt_template = """
#     You are a senior threat intelligence analyst. Your task is to generate a concise, one-page executive summary report
#     based on the threat intelligence data collected in the last 24 hours.

#     The report must be structured as follows:
#     1.  **Key Findings**: A high-level summary of the most significant threats.
#     2.  **Top Threats Details**: A brief description of each of the top threats observed.
#     3.  **General Mitigation Recommendations**: Actionable advice for a general audience to protect against these threats.

#     Here is the summary of the threat data:
#     ---
#     {data_summary}
#     ---

#     Please generate the report now.
#     """

#     prompt = PromptTemplate(
#         input_variables=["data_summary"],
#         template=prompt_template
#     )

#     # Create the LangChain chain
#     chain = LLMChain(llm=llm, prompt=prompt)

#     try:
#         # Run the chain with the data summary
#         report = chain.invoke({"data_summary": data_summary_str})
#         print("Successfully generated threat report.")
#         return report['text']
#     except Exception as e:
#         print(f"An error occurred during report generation: {e}")
#         return f"Failed to generate report. Error: {e}"

# if __name__ == "__main__":
#     print("--- Starting Automated Threat Intelligence Pipeline ---")

#     # 1. Collect Data
#     print("\nStep 1: Fetching latest threat intelligence data...")
#     raw_pulses = get_latest_pulses(OTX_API_KEY)

#     # 2. Process Data
#     print("\nStep 2: Normalizing raw data...")
#     normalized_data = normalize_pulses(raw_pulses)

#     # 3. Analyze and Generate Report
#     print("\nStep 3: Initializing LLM and generating report...")
#     llm = get_llm(GOOGLE_API_KEY)
#     final_report = generate_threat_report(normalized_data, llm)

#     # 4. Display Report
#     print("\n--- Final Threat Intelligence Report ---")
#     print(final_report)
#     print("\n--- Pipeline Finished ---")


# This script is the core of the automated threat intelligence pipeline.
# It uses the LangChain library to interact with a Large Language Model (LLM)
# from Google (Gemini) to generate a human-readable threat report.

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables (like API keys) from a '.env' file.
# This is a secure way to manage sensitive information.
load_dotenv()

# --- PACKAGE IMPORTS ---
# Import the necessary functions from other parts of the 'autoti' package.
# 'get_latest_pulses' is used for data collection.
# 'normalize_pulses' is used for data processing.
from autoti.collection.otx_collector import get_latest_pulses
from autoti.processing.data_normalizer import normalize_pulses


# --- LLM AND API CONFIGURATION ---
# Retrieve the Google API key from environment variables.
# Using .get() provides a default value, which helps prevent errors if the key isn't set.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")


def get_llm(api_key):
    """
    Initializes and configures the Large Language Model (LLM).

    Args:
        api_key (str): The Google API key for authentication.

    Returns:
        ChatGoogleGenerativeAI: An instance of the LLM, ready to be used.
                                Returns None if the API key is missing.
    """
    if api_key in ("YOUR_API_KEY_HERE", None):
        print("ERROR: Google API Key is missing.")
        return None

    # We use Google's 'gemini-2.5-flash' model, which is fast and suitable for summaries.
    # 'temperature=0.2' makes the output more deterministic and focused.
    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-2.5-flash",
        temperature=0.2,
        convert_system_message_to_human=True
    )

def generate_threat_report(normalized_data, llm):
    """
    Generates the threat intelligence report by sending data and a prompt to the LLM.

    Args:
        normalized_data (pd.DataFrame): A DataFrame of processed threat data.
        llm (ChatGoogleGenerativeAI): The initialized LLM instance.

    Returns:
        str: The generated report text. Returns an error message on failure.
    """
    if llm is None:
        return "Report generation failed due to missing LLM configuration."

    if not isinstance(normalized_data, pd.DataFrame) or normalized_data.empty:
        return "No threat data available to generate a report."

    # --- DATA PREPARATION FOR LLM ---
    # We select the top 5 threats to create a concise summary.
    # The DataFrame is converted to a string, which is a format the LLM can easily understand.
    top_threats = normalized_data.head(5)
    data_summary_str = top_threats.to_string(
        columns=['threat_name', 'threat_description', 'ioc_count'],
        index=False
    )

    # --- PROMPT ENGINEERING ---
    # This is the instruction we give to the LLM. A well-crafted prompt is crucial
    # for getting a high-quality response.
    # We tell the LLM its role ('senior threat intelligence analyst'), the desired format,
    # and provide it with the data summary.
    prompt_template = """
    You are a senior threat intelligence analyst. Your task is to generate a concise, one-page executive summary report
    based on the threat intelligence data collected in the last 24 hours.

    The report must be structured as follows:
    1.  **Key Findings**: A high-level summary of the most significant threats.
    2.  **Top Threats Details**: A brief description of each of the top threats observed.
    3.  **General Mitigation Recommendations**: Actionable advice for a general audience to protect against these threats.

    Here is the summary of the threat data:
    ---
    {data_summary}
    ---

    Please generate the report now.
    """

    # We use LangChain's PromptTemplate to structure the prompt and define input variables.
    prompt = PromptTemplate(input_variables=["data_summary"], template=prompt_template)
    
    # An LLMChain combines the prompt and the LLM, creating a runnable component.
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        # We 'invoke' the chain, passing our data summary. This sends the request to the LLM.
        report = chain.invoke({"data_summary": data_summary_str})
        # The actual text is in the 'text' key of the response.
        return report['text']
    except Exception as e:
        # Handle potential errors during the API call.
        return f"Failed to generate report. Error: {e}"


# --- MAIN PIPELINE FUNCTION ---
def run_pipeline():
    """
    Orchestrates the entire process: data collection, processing, and report generation.
    This function is designed to be called by other parts of the application, like the Flask app.
    """
    print("--- Starting Automated Threat Intelligence Pipeline ---")
    
    # Retrieve the OTX API key from environment variables.
    otx_key = os.environ.get("OTX_API_KEY")

    # 1. Collect Data
    print("\nStep 1: Fetching latest threat intelligence data...")
    raw_pulses = get_latest_pulses(otx_key) 

    # 2. Process Data
    print("\nStep 2: Normalizing raw data...")
    normalized_data = normalize_pulses(raw_pulses)

    # 3. Analyze and Generate Report
    print("\nStep 3: Initializing LLM and generating report...")
    llm = get_llm(GOOGLE_API_KEY)
    final_report = generate_threat_report(normalized_data, llm)
    
    print("\n--- Pipeline Finished ---")
    return final_report