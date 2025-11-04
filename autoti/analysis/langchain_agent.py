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


# autoti/analysis/langchain_agent.py

import os
import sys
import pandas as pd
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
# NOTE: load_dotenv() will look for .env in the current working directory, 
# which will be /app (the project root) in the Docker container.
load_dotenv()

# --- IMPORTANT ADJUSTMENT FOR CUSTOM PACKAGE IMPORTS ---
# Since you have a custom package 'autoti', we must ensure its root is on the path
# when a script (like app.py) tries to import from 'autoti.analysis'.
# When running from the root, we ensure the root '.' is in sys.path.
# We'll handle this in the app.py for simplicity.
# You can often remove or comment out complex path manipulation inside the library file:
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the data collection and normalization functions using relative imports 
# or the full package path, assuming the project root is in sys.path.

# Option 1: Full package path (Recommended for clarity, assuming root is on path)
from autoti.collection.otx_collector import get_latest_pulses, OTX_API_KEY
from autoti.processing.data_normalizer import normalize_pulses

# Option 2: Relative imports (Works if lang_chain_agent is the main entry point, but less clean for external Flask app)
# from ..collection.otx_collector import get_latest_pulses, OTX_API_KEY
# from ..processing.data_normalizer import normalize_pulses 


# --- Configuration ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
# OTX_API_KEY is defined in otx_collector.py, but we ensure the value is available
# for the get_latest_pulses function call below.

# ... (rest of get_llm, generate_threat_report functions remain the same) ...
def get_llm(api_key):
    # ... (function body remains the same) ...
    pass

def generate_threat_report(normalized_data, llm):
    # ... (function body remains the same) ...
    pass

# The main function to run the pipeline
def run_pipeline():
    """Encapsulates the full pipeline for easy calling."""
    # Ensure OTX_API_KEY is retrieved here or check its definition in otx_collector.py
    # For robust use, you might retrieve OTX_API_KEY here from os.environ
    otx_key = os.environ.get("OTX_API_KEY") 
    
    print("--- Starting Automated Threat Intelligence Pipeline ---")
    
    # 1. Collect Data
    print("\nStep 1: Fetching latest threat intelligence data...")
    # Pass the key explicitly if otx_collector doesn't load it internally, 
    # otherwise use the imported variable (assuming it's set).
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