import os, requests

def ai_audit(text):
    return (
        "📊 Професійний аудит бізнесу:\n"
        f"Ніша: {text}\n"
        "Точки росту: клієнти, реклама, масштабування.\n\n"
        "Рекомендація: використати AI‑інструменти для залучення нових клієнтів."
    )

def ai_answer(text):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            headers={"Authorization": "Bearer " + os.getenv("HF_API_KEY")},
            json={"inputs": text}
        )
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return "💡 Професійна відповідь:\n" + data[0]["generated_text"]
        else:
            return "⚠️ Немає відповіді від моделі. Перевір токен HF_API_KEY."
    except Exception as e:
        return f"⚠️ Помилка: {str(e)}"
