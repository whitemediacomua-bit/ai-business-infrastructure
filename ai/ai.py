import os, requests

def ai_audit(text):
    return f"📊 Аналіз бізнесу:\n- Ніша: {text}\n- Точки росту: клієнти, реклама, масштабування."

def ai_answer(text):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            headers={"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"},
            json={"inputs": text}
        )
        data = response.json()
        return "💡 Відповідь:\n" + data[0]["generated_text"]
    except Exception:
        return f"💡 Відповідь:\n{text}\n(У безкоштовній версії відповіді обмежені)"
