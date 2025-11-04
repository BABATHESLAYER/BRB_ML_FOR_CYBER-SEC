# FROM python:3.12-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -U google-generativeai langchain-google-genai langchain-core langchain langchain-community
# COPY autoti/ /app/autoti
# CMD ["python3", "-u", "autoti/analysis/langchain_agent.py"]

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container to the root of your project
WORKDIR /app

# 1. Copy setup and requirements files
# Copy requirements.txt, setup.py, and app.py to the working directory /app
COPY requirements.txt .
COPY setup.py .
COPY app.py .

# 2. Install dependencies, including the local 'autoti' package via '-e .'
# NOTE: Removed the redundant RUN pip install -U ... line.
# All needed packages (Gunicorn, Flask, LangChain, and autoti) must be in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U google-generativeai langchain-google-genai langchain-core langchain langchain-community
RUN pip install --no-cache-dir gunicorn

# 3. Copy the custom package code
COPY autoti /app/autoti

# 4. Expose the port where the Flask application runs
EXPOSE 5000

# 5. Command to run the Flask application using Gunicorn
# This is NOT your current CMD, but one that causes this error:
CMD ["gunicorn", "app:app", "--user", "app:app"]
