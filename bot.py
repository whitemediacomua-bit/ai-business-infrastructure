import os
from ai.ai import ai_audit, copilot_answer
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
        ["⚙️ Налаштування чат‑бота"],
        ["💬 Консультація"],
        ["💸 Ціни"],
        ["📝 Промпт‑менеджер"],
        ["📞 Звʼязатися з менеджером"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Вітаю! Я ваш SaaS AI‑маркетолог у Telegram.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу та штучний інтелект.\n\n"
        "Оберіть дію нижче:",
        reply_markup=reply_markup
    )

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

    if text == "🧾 AI‑Аудит бізнесу":
        await update.message.reply_text(
            "🔍 AI‑Аудит бізнесу:\n\n"
            "Опишіть ваш бізнес: ніша, місто, середній чек, чи є реклама.\n"
            "Я дам професійний аналіз і покажу точки росту."
        )
        context.user_data["waiting_audit"] = True
        return

    if text == "💎 AI‑Офер":
        await update.message.reply_text(
            "💎 AI‑Офер:\n\n"
            "Напишіть продукт, цільову аудиторію та головну проблему клієнта.\n"
            "Я сформую сильний офер, який продає."
        )
        return

    if text == "📈 AI‑Ідеї росту":
        await update.message.reply_text(
            "📈 AI‑Ідеї росту:\n\n"
            "Напишіть нішу — я дам 5 стратегій масштабування бізнесу.\n"
            "Отримаєте конкретні кроки для розвитку."
        )
        return

    if text == "📢 AI‑Реклама":
        await update.message.reply_text(
            "📢 AI‑Реклама:\n\n"
            "Я працюю з Meta Ads, Google Ads, TikTok Ads.\n"
            "Напишіть бюджет і нішу — я дам рекомендації для ефективної реклами."
        )
        return

    if text == "🤖 AI‑Автоворонка":
        await update.message.reply_text(
            "🤖 AI‑Автоворонка:\n\n"
            "Я створю AI‑автоворонку: збір лідів, прогрів, комерційна пропозиція та розсилка.\n"
            "Це автоматизує продажі й підвищить конверсію."
        )
        return

    if text == "⚙️ Налаштування чат‑бота":
        await update.message.reply_text(
            "⚙️ Налаштування чат‑бота:\n\n"
            "Я допоможу інтегрувати чат‑бота з сайтом, CRM та каналами.\n"
            "Це зробить ваш бізнес автоматизованим і сучасним."
        )
        return

    if text == "💬 Консультація":
        await update.message.reply_text(
            "💬 Консультація:\n\n"
            "Напишіть ваш номер телефону — ми звʼяжемося.\n"
            "Або телефонуйте напряму: +380671902929."
        )
        return

    if text == "💸 Ціни":
        await update.message.reply_text(
            "💸 Ціни:\n\n"
            "Вартість послуг від 100$. Деталі обговорюємо на консультації.\n"
            "Я підберу оптимальний пакет для вашого бізнесу."
        )
        return

    if text == "📝 Промпт‑менеджер":
        await update.message.reply_text(
            "📝 Промпт‑менеджер:\n\n"
            "Якщо вам потрібна допомога — напишіть: 'Мені потрібна допомога з ...'\n"
            "Я перетворю це у професійний запит до AI, щоб ви отримали найкращу відповідь."
        )
        return

    if text == "📞 Звʼязатися з менеджером":
        await update.message.reply_text(
            "📞 Звʼязатися з менеджером:\n\n"
            "Телефон: +380671902929\n"
            "🌐 Сайт: https://whitemedia.com.ua/"
        )
        return

    if context.user_data.get("waiting_audit"):
        await update.message.reply_text("🔍 Аналізую бізнес...")
        result = ai_audit(text)
        await update.message.reply_text(result)
        context.user_data["waiting_audit"] = False
        return

    # Copilot відповіді (користувачі не бачать слово Copilot)
    answer = copilot_answer(text)
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
