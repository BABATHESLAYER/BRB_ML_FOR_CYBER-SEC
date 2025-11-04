# Automated Threat Intelligence System (AutoTI)

This project is a proof-of-concept for an automated system that collects, processes, and analyzes threat intelligence data to generate concise reports.

## Features

*   **Data Collection:** Fetches the latest threat intelligence pulses from AlienVault OTX.
*   **Data Processing:** Normalizes raw JSON data into a structured pandas DataFrame.
*   **AI-Powered Analysis:** Uses a LangChain agent with an OpenAI model to generate a summary report of the latest threats.
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

3.  **Set your API keys as environment variables:**
    ```bash
    export OTX_API_KEY="your_alienvault_otx_api_key"
    export OPENAI_API_KEY="your_openai_api_key"
    ```

4.  **Run a component script:**
    ```bash
    python3 autoti/collection/otx_collector.py
    ```

## Running with Docker

This application is containerized using Docker for consistent and easy deployment.

1.  **Build the Docker image:**
    From the root of the project directory, run the following command:
    ```bash
    docker build -t autoti-app .
    ```

2.  **Run the Docker container:**
    You must provide your AlienVault OTX and OpenAI API keys as environment variables when running the container.
    ```bash
    docker run --rm \
      -e OTX_API_KEY="your_alienvault_otx_api_key" \
      -e OPENAI_API_KEY="your_openai_api_key" \
      autoti-app
    ```
    The container will start, and the `langchain_agent.py` script will execute, printing the generated threat report to the console.
