import os
from ai.ai import ai_audit
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, get_all_users
from openai import OpenAI

# --- Ключі та токени ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Ініціалізація OpenAI ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Ініціалізація бази ---
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

    website_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Перейти на сайт WhiteMedia", url="https://whitemedia.com.ua/")]
    ])

    await update.message.reply_text(
        "Вітаю 👋 Я ваш AI‑маркетолог.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу та штучний інтелект.\n\n"
        "Оберіть дію нижче або відвідайте наш сайт:",
        reply_markup=website_button
    )

    await update.message.reply_text("📋 Меню:", reply_markup=reply_markup)

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

    # --- Кнопки ---
    if text == "🧾 AI‑Аудит бізнесу":
        await update.message.reply_text("🔍 Опишіть ваш бізнес: ніша, місто, середній чек, чи є реклама.")
        context.user_data["waiting_audit"] = True
        return

    if text == "💎 AI‑Офер":
        await update.message.reply_text("💎 Напишіть продукт, цільову аудиторію та головну проблему клієнта.")
        return

    if text == "📈 AI‑Ідеї росту":
        await update.message.reply_text("📈 Напишіть нішу — я дам 5 стратегій масштабування.")
        return

    if text == "📢 AI‑Реклама":
        await update.message.reply_text("📢 Я працюю з Meta Ads, Google Ads, TikTok Ads.\nНапишіть бюджет і нішу.")
        return

    if text == "🤖 AI‑Автоворонка":
        await update.message.reply_text("🤖 Я створю AI‑автоворонку: збір лідів, прогрів, комерційна пропозиція та розсилка.")
        return

    if text == "💬 Консультація":
        await update.message.reply_text("📞 Напишіть ваш номер телефону — ми звʼяжемося.\nАбо телефонуйте напряму: +380671902929")
        return

    if text == "💸 Ціни":
        await update.message.reply_text("💸 Вартість від 100$. Деталі на консультації.")
        return

    # --- Аудит бізнесу ---
    if context.user_data.get("waiting_audit"):
        await update.message.reply_text("🔍 Аналізую бізнес...")
        result = ai_audit(text)   # виклик OpenAI
        await update.message.reply_text(result)
        context.user_data["waiting_audit"] = False
        return

    # --- Розумні відповіді на будь-які питання ---
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("⚠️ Помилка при генерації відповіді. Перевірте OPENAI_API_KEY.")

# --- RUN ---
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
