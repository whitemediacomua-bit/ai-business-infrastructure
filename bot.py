import os
import random

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from database import create_table, add_user, get_all_users

# --- ENV ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

create_table()

# --- INTENT ANALYSIS ---
def analyze_intent(text):
    text = text.lower()
    if any(word in text for word in ["ціна", "скільки", "вартість"]):
        return "price"
    if any(word in text for word in ["хочу", "потрібно", "замовити"]):
        return "ready"
    if any(word in text for word in ["думаю", "поки що", "цікаво"]):
        return "doubt"
    if any(word in text for word in ["аудит"]):
        return "audit"
    return "other"

def calculate_score(user):
    score = 0
    if user.get("budget_value", 0) >= 1000:
        score += 5
    if user.get("intent") == "ready":
        score += 5
    if user.get("intent") == "price":
        score += 2
    if user.get("intent") == "doubt":
        score -= 2
    return score

# --- START / MENU ---
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

# --- MESSAGE HANDLER ---
user_data = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # === BASIC MENU RESPONSES ===
    if text == "🚀 Консультація":
        await update.message.reply_text("Напишіть ваш номер телефону 📞")
        return

    if text == "📋 Послуги":
        await update.message.reply_text(
            "• Meta Ads\n• Google Ads\n• AI-боти для бізнесу\n"
            "• Автоворонки продажів\n• Текстові креативи\n"
            "• Візуальні креативи\n• Стратегія запуску\n"
            "• Аудит реклами\n• Налаштування аналітики"
        )
        return

    if text == "💰 Ціни":
        await update.message.reply_text("Від 100$. Деталі на консультації.")
        return

    if text == "🎁 Безкоштовний аудит":
        await update.message.reply_text("Напишіть 'аудит' і я зроблю розбір.")
        return

    # === TEXT INTENT PROCESSING ===
    intent = analyze_intent(text)

    # Save user state
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]["intent"] = intent

    # Budget extraction
    import re
    numbers = re.findall(r"\d+", text)
    if numbers:
        budget = int(numbers[0])
        user_data[user_id]["budget_value"] = budget

    score = calculate_score(user_data[user_id])

    # --- HOT LEAD ---
    if score >= 7:
        await update.message.reply_text(
            "🔥 Бачу, що ви готові до серйозного масштабування.\n"
            "Пропоную обговорити стратегію персонально."
        )

        await context.bot.send_message(
            ADMIN_ID,
            f"🔥 HOT LEAD\nID: {user_id}\nДані: {user_data[user_id]}"
        )
        return

    # --- PRICE INTENT ---
    if intent == "price":
        await update.message.reply_text(
            "Вартість залежить від ніші та цілей.\n"
            "Який у вас місячний бюджет на рекламу?"
        )
        return

    # --- DOUBT INTENT ---
    if intent == "doubt":
        await update.message.reply_text(
            "Розумію 🤔\n"
            "Ось приклад: наш клієнт у сфері бʼюті збільшив заявки на 240% за 2 місяці.\n"
            "Чи розглядаєте запуск у найближчий місяць?"
        )
        return

    # --- OTHER ---
    await update.message.reply_text(
        "Розкажіть більше про ваш бізнес і ціль реклами."
    )

# --- BROADCAST ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    message = " ".join(context.args)
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
        except:
            pass
    await update.message.reply_text("📤 Розсилка завершена ✅")

# --- SETUP & RUN ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
