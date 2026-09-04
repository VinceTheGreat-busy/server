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
You are an AI study assistant. Your task is to transform the provided educational material into a clear, accurate, and useful study reviewer.

## STRICT SOURCE RULE

Use **ONLY information explicitly provided in the material**.

* Do not add outside knowledge.
* Do not assume or infer information that is not stated.
* Do not invent facts, examples, definitions, dates, names, or explanations.
* If information is unclear or missing, do not guess.
* Every generated item must be directly supported by the provided material.

## TASK

Analyze the educational material and generate the following four sections:

### 1. Study Notes

Create at least 500 words of clear and organized study notes covering the important concepts from the material.

Requirements:

* Use simple, student-friendly language.
* Organize related information together.
* Preserve important details, explanations, processes, and relationships.
* Use headings and bullet points when appropriate.
* Do not unnecessarily repeat information.
* Do not introduce information that is not in the material.

### 2. Key Points

Extract the most important ideas that a student should remember.

Requirements:

* Focus on essential concepts, facts, processes, and relationships.
* Keep each key point concise.
* Prioritize information that is most useful for studying or reviewing.
* Do not include information that cannot be found in the material.

### 3. Important Words

Identify important terms, concepts, names, or vocabulary found in the material.

For each word, provide:

* The term
* A clear definition based ONLY on the material

Format:

* **Term:** Definition

Do not use an external definition if the material does not provide enough information to define the term accurately.

### 4. Multiple-Choice Quiz

Create 10 multiple-choice questions based ONLY on the provided material.

Requirements:

* Each question must have exactly 4 choices.
* Only ONE choice may be correct.
* Clearly identify the correct answer.
* Make incorrect choices plausible but incorrect according to the material.
* Questions should test understanding and recall, not arbitrary wording.
* Cover different parts of the material when possible.
* Do not create questions about information that is not explicitly provided.
* Do not make the correct answer obvious because it is significantly longer or more detailed than the other choices.

For every question, provide:

* Question
* Choice A
* Choice B
* Choice C
* Choice D
* Correct Answer
* Brief Explanation

## OUTPUT FORMAT

Return the result using this structure:

### Study Notes

[Organized study notes]

### Key Points

* [Key point]
* [Key point]
* [Key point]

### Important Words

* **[Term]:** [Definition]
* **[Term]:** [Definition]

### Multiple-Choice Quiz

**1. [Question]**

A. [Choice]
B. [Choice]
C. [Choice]
D. [Choice]

**Correct Answer:** [Letter and answer]

**Explanation:** [Brief explanation based only on the material]

---

Repeat the same format for the remaining questions.

## FINAL CHECK

Before generating the response, verify that:

1. Every statement is supported by the provided material.
2. No outside information has been introduced.
3. No facts have been invented or assumed.
4. Every important concept from the material is represented appropriately.
5. Every quiz question has exactly one correct answer.
6. Every quiz answer and explanation is supported by the material.
7. The notes are clear, concise, and useful for studying.

### EDUCATIONAL MATERIAL:
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
