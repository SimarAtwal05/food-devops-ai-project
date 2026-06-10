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

def root_cause_agent(state):
    print("STEP 5: ROOT CAUSE AGENT")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Determine root cause.

        Analysis:

        {state['analysis']}
        """
    )
    print("STEP 6: ROOT CAUSE COMPLETE")
    return {
        "root_cause": response.text
    }