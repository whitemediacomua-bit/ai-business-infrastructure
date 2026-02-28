import os
import random
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from database import create_table, add_user, get_all_users

TOKEN = os.getenv("TELEGRAM_TOKEN")

create_table()

def detect_intent(text):
    text = text.lower()

    if any(word in text for word in ["ціна", "скільки", "вартість"]):
        return "price"

    if any(word in text for word in ["реклама", "meta", "google"]):
        return "ads"

    if any(word in text for word in ["бот", "ai"]):
        return "bot"

    if any(word in text for word in ["хочу", "запуск", "працювати"]):
        return "start"

    return "general"


def generate_ai_response(intent):

    responses = {
        "price": [
            "Повний пакет запуску під ключ — 1200$.\nВключає рекламу, креативи та аналітику.",
            "Базовий запуск стартує від 100$. Хочете підберемо варіант під вас?"
        ],

        "ads": [
            "Ми запускаємо Meta Ads та Google Ads з аналітикою.",
            "Яка у вас ніша та бюджет?"
        ],

        "bot": [
            "AI-боти автоматично обробляють заявки 24/7.",
            "Хочете бот для продажів чи підтримки?"
        ],

        "start": [
            "Супер 👌 Розкажіть про вашу нішу.",
            "Яка ваша основна ціль зараз?"
        ],

        "general": [
            "Розкажіть трохи більше про ваш бізнес.",
            "Я підкажу оптимальне рішення для вас."
        ]
    }

    return random.choice(responses[intent])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)

    keyboard = [
        ["🚀 Консультація"],
        ["📋 Послуги"],
        ["💰 Ціни"],
        ["🎁 Безкоштовний аудит"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # КНОПКА НА САЙТ
    website_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Перейти на сайт", url="https://whitemedia.com.ua/")]
])
    await update.message.reply_text(
        "Вітаю! Я AI-консультант для бізнесу 🚀 або перейдіть на сайт:",
        reply_markup=website_button
     )
    await update.message.reply_text(
        "Вітаю 👋\nЯ допомагаю бізнесу отримувати клієнтів через рекламу та AI.\n\nОберіть, що вас цікавить:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 Консультація":
        await update.message.reply_text("Напишіть ваш номер телефону 📞")
        return

    elif text == "📦 Послуги":
        await update.message.reply_text(
            "🔹 Meta Ads\n"
            "🔹 Google Ads\n"
            "🔹 AI-боти для бізнесу\n"
            "🔹 Автоворонки продажів\n"
            "🔹 Текстові креативи\n"
            "🔹 Візуальні креативи\n"
            "🔹 Стратегія запуску\n"
            "🔹 Аудит реклами\n"
            "🔹 Налаштування аналітики"
        )
        return

    elif text == "💰 Ціни":
        await update.message.reply_text("Від 100$. Деталі на консультації.")
        return

    elif text == "🎁 Безкоштовний аудит":
        await update.message.reply_text("Напишіть 'аудит' і я зроблю розбір.")
        return

    # ---- ОБРОБКА ЗВИЧАЙНОГО ТЕКСТУ ----

    text_lower = text.lower()

    if "реклама" in text_lower:
        await update.message.reply_text(
            "Ми запускаємо Meta Ads та Google Ads.\n"
            "Працюємо під ключ з аналітикою та оптимізацією.\n"
            "Яка у вас ніша?"
        )
        return

    await update.message.reply_text(
        "Напишіть, будь ласка, яка у вас ніша і який бюджет на рекламу?"
    )
    
# ----- ПСЕВДО AI (якщо нічого не спрацювало) -----

intent = detect_intent(text)
reply = generate_ai_response(intent)
await update.message.reply_text(reply)
return

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    message = " ".join(context.args)

    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
        except:
            pass

    await update.message.reply_text("Розсилка завершена ✅")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling(drop_pending_updates=True)
