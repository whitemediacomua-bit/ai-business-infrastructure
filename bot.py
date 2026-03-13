import os
from ai.ai import ai_audit, copilot_answer
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, get_all_users

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

create_table()
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)

    keyboard = [
        ["🧾 AI‑Аудит бізнесу"],
        ["💎 AI‑Офер"],
        ["📈 AI‑Ідеї росту"],
        ["📢 AI‑Реклама"],
        ["🤖 AI‑Автоворонка"],
        ["⚙️ Налаштування чат‑бота"],
        ["💬 Консультація"],
        ["💸 Ціни"],
        ["📝 Промпт‑менеджер"],
        ["📞 Звʼязатися з менеджером"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Вітаю 👋 Я ваш AI‑маркетолог.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу та штучний інтелект.\n\n"
        "Оберіть дію нижче:",
        reply_markup=reply_markup
    )

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🧾 AI‑Аудит бізнесу":
        await update.message.reply_text("🔍 Опишіть ваш бізнес: ніша, місто, середній чек, чи є реклама.")
        context.user_data["waiting_audit"] = True
        return

    if text == "⚙️ Налаштування чат‑бота":
        await update.message.reply_text("⚙️ Тут можна налаштувати інтеграцію з сайтом, CRM та каналами.")
        return

    if text == "💬 Консультація":
        await update.message.reply_text("📞 Напишіть ваш номер телефону — ми звʼяжемося.\nАбо телефонуйте напряму: +380671902929")
        return

    if text == "📝 Промпт‑менеджер":
        await update.message.reply_text(
            "📝 Промпт‑менеджер допоможе вам сформулювати запит правильно.\n\n"
            "Напишіть: 'Мені потрібна допомога з ...'\n"
            "Я перетворю це у професійний запит до AI."
        )
        return

    if text == "📞 Звʼязатися з менеджером":
        await update.message.reply_text("📞 Телефон: +380671902929\n🌐 Сайт: https://whitemedia.com.ua/")
        return

    if context.user_data.get("waiting_audit"):
        await update.message.reply_text("🔍 Аналізую бізнес...")
        result = ai_audit(text)
        await update.message.reply_text(result)
        context.user_data["waiting_audit"] = False
        return

    # Copilot відповіді
    answer = copilot_answer(text)
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
