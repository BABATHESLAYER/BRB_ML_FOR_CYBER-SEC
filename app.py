from flask import Flask, render_template_string
import sys
import os

# Ensure the project root is in the Python path to allow imports like 'autoti.analysis...'
# This is necessary because we are importing from a sub-package.
# The Docker WORKDIR is /app, so we add /app (the current directory) to the path.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the pipeline function from your custom package structure
# This assumes your main script is autoti/analysis/langchain_agent.py
# Initialize a variable to hold import errors globally
IMPORT_ERROR_MESSAGE = None

try:
    from autoti.analysis.langchain_agent import run_pipeline
except ImportError as e:
    # Store the error message in the global variable
    IMPORT_ERROR_MESSAGE = str(e)
    
    print(f"FATAL ERROR: Could not import run_pipeline. Error: {IMPORT_ERROR_MESSAGE}")
    
    # Define the dummy function using the stored variable
    def run_pipeline():
        # Use the global variable here
        return f"Application initialization failed. Import error: {IMPORT_ERROR_MESSAGE}"


app = Flask(__name__)

# Simple HTML template for the report display
REPORT_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Threat Intelligence Report</title>
    <style>
        body { 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 20px;
            background-color: #f0f4f8;
            color: #1f2937;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        h1 { 
            color: #111827; 
            font-size: 2.25rem;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        pre { 
            background-color: #1f2937; 
            color: #d1d5db; 
            padding: 20px; 
            border-radius: 8px;
            white-space: pre-wrap; 
            word-wrap: break-word; 
            line-height: 1.6;
        }
        .error {
            color: #b91c1c;
            background-color: #fee2e2;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #fca5a5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Automated Threat Intelligence Executive Summary</h1>
        <p>Report generated on demand using OTX data and Gemini LLM analysis.</p>
        <pre>{{ report_content }}</pre>
    </div>
</body>
</html>
"""

@app.route('/')
def report():
    """Renders the threat intelligence report by running the full pipeline."""
    try:
        # Run the full pipeline
        print("Starting pipeline for web request...")
        report_text = run_pipeline()
    except Exception as e:
        report_text = f"<div class='error'><strong>Report Generation Error!</strong><br>The pipeline failed to execute.<br>Error: {e}</div>"
        print(f"Flask App Error: {e}")

    return render_template_string(REPORT_TEMPLATE, report_content=report_text)

if __name__ == '__main__':
    # Flask will be run by gunicorn in the Docker container, 
    # but this is useful for local testing.
    app.run(host='0.0.0.0', port=5000)
