import os, requests

def ai_audit(text):
    return f"📊 Професійний аудит бізнесу:\n- Ніша: {text}\n- Точки росту: клієнти, реклама, масштабування.\n\nРекомендація: використати AI‑інструменти для залучення нових клієнтів."

def ai_answer(text):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            headers={"Authorization": f"Bearer " + os.getenv("HF_API_KEY")},
            json={"inputs": text}
        )
        data = response.json()
        return "💡 Професійна відповідь:\n" + data[0]["generated_text"]
    except Exception:
        return "⚠️ Тимчасово немає AI‑відповіді. Перевір токен HF_API_KEY."
