import os, requests

def ai_audit(text):
    return (
        "🧾 Професійний AI-аудит бізнесу:\n"
        f"Ніша: {text}\n"
        "Точки росту: клієнти, реклама, масштабування.\n"
        "Рекомендація: використати AI‑інструменти для залучення нових клієнтів. Ви можете звернутися до нас!"
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

def ai_idea(text):
    return "💡 AI‑Ідейка:\nНейромережі згенерує десятки ідей для контенту, реклами та розвитку бренду."

def ai_website(text):
    return "🌐 Розробка сайтів з AI:\nСучасні сайти, які самі вчаться продавати завдяки AI."

def ai_hosting(text):
    return "⚡ Хостинг та AI‑підтримка:\nШвидкість, безпека та моніторинг вашого сайту 24/7."

def ai_ads(text):
    return "📈 AI‑реклама та Meta Ads:\nAI аналізує аудиторію, створює креативи та оптимізує бюджети."

def ai_chatbot(text):
    return "💬 AI‑чат‑боти під ключ:\nРозумні боти для Telegram, Instagram та сайтів."

def ai_analytics(text):
    return "📊 Аналітика та Бізнес‑AI:\nПрогнозування продажів та звіти для повної картини бізнесу."

def ai_mailing(text):
    return "📧 AI‑розсилки:\nПерсоналізовані повідомлення для кожного потенційного клієнта на ID в telegram."

def ai_seo(text):
    return (
        "🔎 AI‑SEO Оптимізація:\n"
        "AI аналізує ключові слова, конкурентів та структуру сайту.\n"
        "Ми створюємо оптимізований контент і технічні рекомендації,\n"
        "щоб ваш сайт піднімався у видачі Google."
    )
