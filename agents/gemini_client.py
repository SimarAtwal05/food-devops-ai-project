import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(
    api_key=api_key
)

MODELS_TO_TRY = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]


def generate_with_fallback(prompt: str):

    last_error = None

    for model_name in MODELS_TO_TRY:

        try:

            print(
                f"Trying model: {model_name}"
            )

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if not response.text:
                raise ValueError(
                    "Empty response"
                )

            return response.text

        except Exception as error:

            print(
                f"Model failed: {model_name}"
            )

            print(error)

            last_error = error

    raise last_error