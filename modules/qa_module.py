# modules/qa_module.py

import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def answer_question(question, context):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=f"{context}\n\nQ: {question}\nA:",
        max_tokens=100
    )
    return response.choices[0].text.strip()
