# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY autoti/ /app/autoti

# API keys should be passed in at runtime as environment variables.
# Example:
# docker run --rm \
#   -e OTX_API_KEY="your_alienvault_otx_api_key" \
#   -e GOOGLE_API_KEY="your_google_api_key" \
#   autoti-app

# Run the langchain_agent.py script when the container launches
# This will demonstrate the full pipeline: collect, normalize, and report.
# For a real-world scenario, you might have separate services or a script that orchestrates these calls.
CMD ["python3", "-u", "autoti/analysis/langchain_agent.py"]
