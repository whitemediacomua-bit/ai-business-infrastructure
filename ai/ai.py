import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_audit(text):
    prompt = f"""
    Ти маркетинговий експерт.
    Проаналізуй бізнес і дай:
    1. головну проблему
    2. 3 точки росту
    3. ідею реклами
    Бізнес: {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
