import os
from dotenv import load_dotenv
from google import genai
from agents.gemini_client import (
    generate_with_fallback
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def log_analyzer(state):
    print("STEP 1: ENTERED LOG ANALYZER")

    with open("logs/error.log", "r") as f:
        log_data = f.read()
    print("STEP 2: READ LOG FILE")

    print("STEP 3: CALLING GEMINI")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Analyze this application error.

        Return:
        - Error Type
        - File
        - Line
        - Explanation

        Error:

        {log_data}
        """
    )
    print("STEP 4: GEMINI RETURNED")
    return {
        "analysis": response.text
    }