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

def fix_generator(state):
    print("STEP 7: FIX GENERATOR")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Generate a fix.

        Root Cause:

        {state['root_cause']}

        Return:
        - Corrected code
        - Explanation

        Keep response concise.
        """
    )
    print("STEP 8: FIX GENERATED")
    patch = response.text

    with open(
        "patches/fix.diff",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(patch)

    return {
        "patch": patch
    }