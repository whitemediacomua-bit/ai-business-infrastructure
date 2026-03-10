import os
import re
from ai.ai import ai_audit
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, get_all_users

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

create_table()
user_data = {}

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    keyboard = [
        ["🧾 AI‑Аудит бізнесу"],
        ["💎 AI‑Офер"],
        ["📈 AI‑Ідеї росту"],
        ["📢 AI‑Реклама"],
        ["🤖 AI‑Автоворонка"],
        ["💬 Консультація"],
        ["💸 Ціни"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Вітаю 👋 Я ваш AI‑маркетолог.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу та штучний інтелект.\n\n"
        "Оберіть дію:", reply_markup=reply_markup
    )

# --- AUDIT ---
async def audit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧾 AI‑Аудит бізнесу\n\n"
        "Опишіть ваш бізнес:\n"
        "• Ніша\n• Місто\n• Середній чек\n• Чи є реклама\n\n"
        "Я зроблю розбір і покажу точки росту."
    )
    context.user_data["waiting_audit"] = True

# --- BROADCAST ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У вас немає доступу")
        return
    users = get_all_users()
    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("Напишіть текст після команди")
        return
    sent = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
            sent += 1
        except:
            pass
    await update.message.reply_text(f"👥 Відправлено {sent} користувачам")

# --- HANDLE ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("waiting_audit"):
        await update.message.reply_text("🔍 Аналізую бізнес...")
        result = ai_audit(text)
        await update.message.reply_text(result)
        context.user_data["waiting_audit"] = False
        return

    # --- Кнопки меню ---
    if text == "🧾 AI‑Аудит бізнесу":
        await update.message.reply_text(
            "🧾 Опишіть ваш бізнес:\n• Ніша\n• Місто\n• Середній чек\n• Чи є реклама\n\nЯ зроблю розбір і покажу точки росту."
        )
        context.user_data["waiting_audit"] = True
        return

    if text == "💎 AI‑Офер":
        await update.message.reply_text(
            "💎 Напишіть ваш продукт, цільову аудиторію та головну проблему клієнта — я сформую сильний продажний офер."
        )
        return

    if text == "📈 AI‑Ідеї росту":
        await update.message.reply_text(
            "📈 Напишіть нішу — я дам 5 стратегій масштабування."
        )
        return

    if text == "📢 AI‑Реклама":
        await update.message.reply_text(
            "📢 Я працюю з:\n• Meta Ads\n• Google Ads\n• TikTok Ads\n\nНапишіть бюджет і нішу — підкажу стратегію запуску."
        )
        return

    if text == "🤖 AI‑Автоворонка":
        await update.message.reply_text(
            "🤖 Я створю AI‑автоворонку: збір лідів, прогрів, комерційна пропозиція та автоматична розсилка."
        )
        return

    if text == "💬 Консультація":
        await update.message.reply_text("📞 Напишіть ваш номер телефону — ми звʼяжемося для персональної консультації.")
        return

    if text == "💸 Ціни":
        await update.message.reply_text("💸 Вартість від 100$. Деталі на консультації.")
        return

    # --- Якщо нічого не співпало ---
    await update.message.reply_text("Розкажіть більше про ваш бізнес і ціль реклами.")

# --- RUN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audit", audit))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
