import os
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_openai import ChatOpenAI


# --- Configuration ---
# Your OpenAI API Key.
# It's recommended to use an environment variable for security.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

def get_llm(api_key):
    """Initializes and returns the ChatOpenAI model."""
    if api_key == "YOUR_API_KEY_HERE":
        print("ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual OpenAI API key.")
        return None

    # Initialize the LLM - we'll use OpenAI's gpt-3.5-turbo as a default
    return ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.2  # Low temperature for more deterministic, factual output
    )

def generate_threat_report(normalized_data, llm):
    """
    Generates a concise threat intelligence report using LangChain and an LLM.

    Args:
        normalized_data (pd.DataFrame): A DataFrame with normalized threat data.
        llm (ChatOpenAI): The initialized LangChain LLM.

    Returns:
        str: The generated threat intelligence report.
             Returns an error message if report generation fails.
    """
    if llm is None:
        return "Report generation failed due to missing LLM configuration."

    if normalized_data.empty:
        return "No threat data available to generate a report."

    # Convert the DataFrame to a string format that's easy for the LLM to parse.
    # We'll use a summary of the top threats.
    top_threats = normalized_data.head(5)
    data_summary_str = top_threats.to_string(
        columns=['threat_name', 'threat_description', 'ioc_count'],
        index=False
    )

    # --- Prompt Engineering ---
    # This is the core of the agent's logic. We instruct the LLM on its role,
    # the format of the output, and what data to use.
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

    prompt = PromptTemplate(
        input_variables=["data_summary"],
        template=prompt_template
    )

    # Create the LangChain chain
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        # Run the chain with the data summary
        report = chain.invoke({"data_summary": data_summary_str})
        print("Successfully generated threat report.")
        return report['text']
    except Exception as e:
        print(f"An error occurred during report generation: {e}")
        return f"Failed to generate report. Error: {e}"

if __name__ == "__main__":
    # --- Sample Normalized Data (for testing) ---
    # This simulates the input from data_normalizer.py
    sample_normalized_data = pd.DataFrame({
        'pulse_id': ['668ba07c0823521f753c8c87', '668ba07c0823521f753c8c88'],
        'threat_name': ["Malicious IPs related to Phishing Campaign", "Fake Browser Update (SocGholish)"],
        'threat_description': [
            "A new set of IPs hosting phishing sites targeting financial institutions.",
            "SocGholish malware being distributed via fake browser update prompts on compromised websites."
        ],
        'ioc_count': [2, 1]
    })

    print("--- Initializing LLM and Generating Threat Report ---")

    # Initialize the LLM
    llm = get_llm(OPENAI_API_KEY)

    # Generate the report
    final_report = generate_threat_report(sample_normalized_data, llm)

    print("\n--- Generated Report ---")
    print(final_report)
