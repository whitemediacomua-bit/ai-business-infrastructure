import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, get_all_users
from ai.ai import ask_ai

TOKEN = os.getenv("TELEGRAM_TOKEN")

create_table()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🚀 Консультація"],
        ["📈 Послуги"],
        ["💰 Ціни"],
        ["🎁 Безкоштовний аудит"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Вітаю 👋\nЯ допомагаю бізнесу отримувати клієнтів через рекламу та AI.\n\nОберіть, що вас цікавить:",
        reply_markup=reply_markup
    )
    user = update.effective_user
    add_user(user.id, user.username)
    await update.message.reply_text("Вітаю! Я AI-консультант для бізнесу 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    answer = ask_ai(user_message)
    await update.message.reply_text(answer)

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
from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling(drop_pending_updates=True)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 Консультація":
        await update.message.reply_text("Напишіть ваш номер телефону, і я зв’яжусь з вами 📞")

    elif text == "📈 Послуги":
        await update.message.reply_text("Я запускаю рекламу Meta Ads, Google Ads та створюю AI-ботів.")

    elif text == "💰 Ціни":
        await update.message.reply_text("Ціни стартують від 300$. Деталі — на консультації.")

    elif text == "🎁 Безкоштовний аудит":
        await update.message.reply_text("Напишіть 'аудит', і я проведу безкоштовний розбір вашої реклами.")
