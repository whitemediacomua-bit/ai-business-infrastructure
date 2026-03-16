import os
from ai import ai_audit, ai_answer
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, get_all_users

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

create_table()

# 🔑 Професійне меню з твоїми послугами
keyboard = [
    ["🌐 Розробка сайтів", "☁️ Хостинг"],
    ["📢 AI‑Реклама", "🤖 Чат‑бот під ключ"],
    ["📊 AI‑Аудит бізнесу", "💌 Розсилки"],
    ["📝 Промпт‑менеджер", "📞 Звʼязатися з менеджером"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🟢 Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    await update.message.reply_text(
        "👋 Вітаю! Це професійний AI‑чат‑бот від WhiteMedia.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу, сайти та штучний інтелект.\n\n"
        "Оберіть послугу нижче:",
        reply_markup=reply_markup
    )

# 📢 Розсилка
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У вас немає доступу")
        return
    users = get_all_users()
    message = " ".join(context.args)
    sent = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
            sent += 1
        except:
            pass
    await update.message.reply_text(f"👥 Відправлено {sent} користувачам")

# 🔧 Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🌐 Розробка сайтів":
        await update.message.reply_text(
            "🌐 Ми створюємо сучасні сайти з AI‑інтеграцією, які приносять клієнтів.\n"
            "Замовте консультацію вже сьогодні!",
            reply_markup=reply_markup
        )
        return

    if text == "☁️ Хостинг":
        await update.message.reply_text(
            "☁️ Надійний хостинг та підтримка для вашого бізнесу.\n"
            "Ваш сайт завжди онлайн.",
            reply_markup=reply_markup
        )
        return

    if text == "📢 AI‑Реклама":
        await update.message.reply_text(
            "📢 AI‑реклама допоможе вам отримати більше заявок за менший бюджет.\n"
            "Ми налаштовуємо таргетинг під ключ.",
            reply_markup=reply_markup
        )
        return

    if text == "🤖 Чат‑бот під ключ":
        await update.message.reply_text(
            "🤖 Ми створюємо чат‑ботів, які збирають ліди, роблять розсилки та інтегруються з CRM.\n"
            "Ваш бізнес працює на автопілоті.",
            reply_markup=reply_markup
        )
        return

    if text == "📊 AI‑Аудит бізнесу":
        await update.message.reply_text(
            "📊 Опишіть ваш бізнес: ніша, місто, середній чек, чи є реклама.",
            reply_markup=reply_markup
        )
        context.user_data["waiting_audit"] = True
        return

    if context.user_data.get("waiting_audit"):
        await update.message.reply_text("🔍 Аналізую бізнес...", reply_markup=reply_markup)
        result = ai_audit(text)
        await update.message.reply_text(result, reply_markup=reply_markup)
        context.user_data["waiting_audit"] = False
        return

    if text == "💌 Розсилки":
        await update.message.reply_text(
            "💌 Ми налаштовуємо автоматичні розсилки для прогріву клієнтів.\n"
            "Ваші клієнти завжди на звʼязку.",
            reply_markup=reply_markup
        )
        return

    if text == "📝 Промпт‑менеджер":
        await update.message.reply_text(
            "📝 Ми створюємо професійні AI‑промпти для маркетингу, реклами та контенту.\n"
            "Ваш бізнес отримує готові інструменти.",
            reply_markup=reply_markup
        )
        return

    if text == "📞 Звʼязатися з менеджером":
        await update.message.reply_text(

> Дарья ✌️:
"📞 Телефон: +380671902929\n🌐 Сайт: https://whitemedia.com.ua/\n\n"
            "Звертайтесь для консультації!",
            reply_markup=reply_markup
        )
        return

    # AI‑відповідь
    answer = ai_answer(text)
    await update.message.reply_text(answer, reply_markup=reply_markup)

# 🚀 Запуск
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
