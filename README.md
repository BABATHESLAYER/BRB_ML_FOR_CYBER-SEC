# Automated Threat Intelligence System (AutoTI)

This project is a proof-of-concept for an automated system that collects, processes, and analyzes threat intelligence data to generate concise reports.

## Features

*   **Data Collection:** Fetches the latest threat intelligence pulses from AlienVault OTX.
*   **Data Processing:** Normalizes raw JSON data into a structured pandas DataFrame.
*   **AI-Powered Analysis:** Uses a LangChain agent with Google's Gemini model to generate a summary report of the latest threats.
*   **Containerized:** Docker support for easy setup and deployment.

## Project Structure

```
.
├── autoti/
│   ├── collection/
│   │   └── otx_collector.py
│   ├── processing/
│   │   └── data_normalizer.py
│   ├── analysis/
│   │   └── langchain_agent.py
│   └── ...
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup and Installation (Local)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure your API keys:**
    Create a `.env` file by copying the example template:
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and replace the placeholder values with your actual API keys.

4.  **Run the main pipeline:**
    ```bash
    python3 autoti/analysis/langchain_agent.py
    ```

## Running with Docker

This application is containerized using Docker for consistent and easy deployment.

1.  **Build the Docker image:**
    From the root of the project directory, run the following command:
    ```bash
    docker build -t autoti-app .
    ```

2.  **Run the Docker container:**
    You must provide your AlienVault OTX and Google API keys as environment variables when running the container.
    ```bash
    docker run --rm \
      -e OTX_API_KEY="your_alienvault_otx_api_key" \
      -e GOOGLE_API_KEY="your_google_api_key" \
      autoti-app
    ```
    The container will start, and the `langchain_agent.py` script will execute, printing the generated threat report to the console.
