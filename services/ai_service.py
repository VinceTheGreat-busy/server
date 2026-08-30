import os
from google import genai

from schemas.ai_schema import StudyMaterial
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def test_ai():

    response = client.models.generate_content(
        model="gemini-3.6-flash", contents="Hello, how are you?"
    )

    return response.text


def generate_study_material(text: str):

    prompt = f"""
You are an AI study assistant.

Analyze the following educational material.

Create:
- Clear study notes
- Important key points
- Important words with definitions
- Multiple-choice quiz questions

Only use information found in the provided material.

MATERIAL:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": StudyMaterial.model_json_schema(),
        },
    )

    return StudyMaterial.model_validate_json(response.text)
