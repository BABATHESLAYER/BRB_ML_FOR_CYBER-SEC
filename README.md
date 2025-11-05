# Automated Threat Intelligence System (AutoTI)

## Project Overview

AutoTI is an automated system that collects, processes, and analyzes threat intelligence data to generate concise, human-readable reports. It leverages AlienVault OTX for data collection and a Large Language Model (LLM) through LangChain for analysis, providing a streamlined workflow for threat intelligence.

## Features

- **Automated Data Collection:** Fetches the latest threat intelligence "pulses" from AlienVault OTX.
- **Structured Data Processing:** Normalizes raw JSON data into a clean, structured pandas DataFrame, making it suitable for analysis.
- **AI-Powered Analysis:** Utilizes a LangChain agent with a Google Gemini LLM to generate executive summary reports of the latest threats.
- **Web Interface:** Provides a simple Flask-based web interface to view the generated reports.
- **Containerized Deployment:** Includes a Dockerfile for easy and consistent setup and deployment.

## Project Structure

```
.
├── autoti/
│   ├── __init__.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── langchain_agent.py  # Core logic for LLM interaction and report generation.
│   ├── collection/
│   │   ├── __init__.py
│   │   └── otx_collector.py      # Fetches data from the AlienVault OTX API.
│   └── processing/
│       ├── __init__.py
│       └── data_normalizer.py  # Cleans and structures the raw data.
├── .dockerignore
├── .env.example                # Example environment file.
├── .gitignore
├── Dockerfile                  # For building the Docker container.
├── README.md                   # This file.
├── app.py                      # The Flask web application.
├── requirements.txt            # Python dependencies.
└── setup.py                    # Setup script for the autoti package.
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Create a `.env` file by copying the example:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and add your actual API keys for AlienVault OTX and Google.

### Running the Application

There are two ways to run the application:

1.  **As a Command-Line Tool:**
    To run the entire pipeline and print the report to the console:
    ```bash
    python autoti/analysis/langchain_agent.py
    ```

2.  **As a Web Application:**
    To start the Flask web server and view the report in your browser:
    ```bash
    flask run
    ```
    The application will be available at `http://localhost:5000`.

## Running with Docker

The application is containerized for easy deployment.

1.  **Build the Docker image:**
    ```bash
    docker build -t autoti-app .
    ```

2.  **Run the Docker container:**
    You must provide your API keys as environment variables.
    ```bash
    docker run -p 5000:5000 --env-file .env autoti-app
    ```
    The web application will be accessible at `http://localhost:5000`.
