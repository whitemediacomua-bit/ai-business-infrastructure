import os, requests

def ai_audit(text):
    return (
        "🧾 Професійний аудит бізнесу:\n"
        f"Ніша: {text}\n"
        "Точки росту: клієнти, реклама, масштабування.\n\n"
        "Рекомендація: використати AI‑інструменти для залучення нових клієнтів."
    )

def ai_answer(text):
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": "Bearer " + os.getenv("DEEPSEEK_API_KEY")},
            json={
                "model": "deepseek-chat",   # безкоштовна модель
                "messages": [{"role": "user", "content": text}]
            }
        )
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return "💬 Професійна відповідь:\n" + data["choices"][0]["message"]["content"]
        else:
            return "⚠️ Немає відповіді від моделі. Перевір токен DEEPSEEK_API_KEY."
    except Exception as e:
        return f"⚠️ Помилка: {str(e)}"
