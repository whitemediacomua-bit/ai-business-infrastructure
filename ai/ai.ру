import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_ai(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Ти професійний експерт з маркетингу, продажів та автоматизації бізнесу."
            },
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
