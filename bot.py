import os
from ai.ai import ai_audit, ai_answer
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_table, add_user, add_request, get_all_users

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

create_table()

# 🔑 Меню
keyboard = [
    ["📊 AI-Аудит бізнесу", "💡 AI-Ідейка"],
    ["🌐 Розробка сайтів", "☁️ Хостинг"],
    ["📈 AI-Реклама", "💬 AI-Чат-боти"],
    ["📊 AI-Аналітика", "📧 AI-Розсилки"],
    ["🔎 AI-SEO Оптимізація", "📝 Промпт-менеджер"],
    ["📞 Звʼязатися з менеджером", "📦 Комерційна пропозиція"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🟢 Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # ✅ Збереження в базу
    add_user(user.id, user.username)

    # 👋 Користувачу
    await update.message.reply_text(
        "👋 Вітаю! Це професійний AI-чат-бот від WhiteMedia.\n\n"
        "Я допомагаю бізнесу отримувати клієнтів через рекламу, сайти та AI.\n\n"
        "Оберіть послугу:",
        reply_markup=reply_markup
    )

    # 🚨 Адміну
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🚨 Новий користувач\nID: {user.id}\nUsername: @{user.username}"
    )

# 📢 Розсилка
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users = get_all_users()
    message = " ".join(context.args)

    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
        except:
            pass

    await update.message.reply_text("✅ Розсилка завершена")


# 🔧 Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    # 🔔 Повідомлення адміну про кожну дію
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 {user.id} (@{user.username}) натиснув:\n{text}"
    )

    if text == "📊 AI-Аудит бізнесу":
        context.user_data["waiting_audit"] = True
        await update.message.reply_text(
            "📊 Ми аналізуємо Вашу нішу, конкурентів та точки росту.\n"
            "Отримайте готову стратегію розвитку бізнесу за допомогою AI.\n"
            "Опишіть ваш бізнес: ніша, місто, середній чек, чи є реклама.",
            reply_markup=reply_markup
        )
        return
        
    if context.user_data.get("waiting_audit"):
        result = ai_audit(text)
        add_request(user.id, "audit", text)
        await update.message.reply_text(result, reply_markup=reply_markup)
        context.user_data["waiting_audit"] = False
        return

    if text == "💡 AI-Ідейка":
        add_request(user.id, "idea", text)
        await update.message.reply_text(
            "💡 Нейромережа згенерує десятки ідей для контенту, реклами та розвитку бренду.\n"
            "Ви отримаєте натхнення за хвилини.\n\n"
            "Опишіть ваш бізнес:",
            reply_markup=reply_markup
        )
        return

    if text == "🌐 Розробка сайтів":
        add_request(user.id, "website", text)
        await update.message.reply_text(
            "🌐 Ми створюємо сучасні сайти з AI-інтеграцією, які не просто існують, а реально продають приносять клієнтів.\n"
            "Замовте консультацію вже сьогодні!",
            reply_markup=reply_markup
        )
        return

    if text == "☁️ Хостинг":
        add_request(user.id, "hosting", text)
        await update.message.reply_text(
            "☁️ Надійний хостинг із AI-моніторингом.\nВаш сайт завжи онлайн, швидкий та захищенний.\n"
            "Професійна підтримка для Вашого бізнесу.",
            reply_markup=reply_markup
        )
        return

    if text == "📈 AI-Реклама":
        add_request(user.id, "ads", text)
        await update.message.reply_text(
            "📈 AI аналізує аудиторію, створює креативи та оптимізує бюджети.\n"
            "Вам отримати більше заявок за менший бюджет.\n"
            "Ми налаштовуємо таргетинг під ключ.",
            reply_markup=reply_markup
        )
        return

    if text == "💬 AI-Чат-боти":
        add_request(user.id, "chatbot", text)
        await update.message.reply_text(
            "💬 AI-Чат-боти під ключ.\n"
            "Консультують клієнтів, збирають ліди, приймають заявки, продають 24/7, роблять розсилки та інтегруються з CRM.\n"
            "Ваш бізнес працює на автопілоті.",
            reply_markup=reply_markup
        )
        return

    if text == "📊 AI-Аналітика":
        add_request(user.id, "analytics", text)
        await update.message.reply_text(
            "📊 AI_Аналітика допоможе прогнозувати продажі, аналізувати данні та показувати Вам повну картину бізнесу.\n"
            "Ви отримуєте зрозумілі звіти та прогнози для прийняття рішень.\n\n"
            "Опишіть ваш запит:",
            reply_markup=reply_markup
        )

    if text == "🔎 AI-SEO Оптимізація":
        add_request(user.id, "seo", text)
        await update.message.reply_text(
            "🔎 AI-SEO Оптимізація:\n"
            "Ми оптимізуємо ваш сайт під пошукові системи за допомогою AI.\n"
            "Аналіз ключових слів, створення контенту та технічна оптимізація.\n"
            "Щоб Ваш бізнес був на перших позиціях у Google.",
            reply_markup=reply_markup
        )
        return

    if text == "📧 AI-Розсилки":
        add_request(user.id, "mailing", text)
        await update.message.reply_text(
            "📧 Ми налаштовуємо автоматичні розсилки для прогріву клієнтів.\n"
            "Персоналізовані повідомлення для кожного клієнта.\n"
            "Конверсія зростає в рази.\n"
            "Ваші клієнти завжди на звʼязку.",
            reply_markup=reply_markup
        )
        return

    if text == "📦 Комерційна пропозиція":
        add_request(user.id, "commercial-offer", text)
        await update.message.reply_text(
            "📦 Пакет послуг WhiteMedia — AI-маркетинг для бізнесу:\n\n"
            "📊 AI-Аудит бізнесу — аналіз ніші, конкурентів та стратегія розвитку.\n"
            "💰 Ціна: від 100$ до 300$\n\n"
            "💡 AI-Ідейка — генерація десятків ідей для контенту та реклами.\n"
            "💰 Ціна: від 80$ до 300$\n\n"
            "🌐 Розробка сайтів — сучасні сайти з AI-інтеграцією, які реально продають.\n"
            "💰 Ціна: від 500$ до 1800$\n\n"
            "⚡ Хостинг — швидкий, захищений, з AI-моніторингом 24/7.\n"
            "💰 Ціна: від 50$ до 150$ на місяць\n\n"
            "📈 AI-Реклама — аналіз аудиторії, створення креативів, оптимізація бюджету.\n"
            "💰 Ціна: від 200$ до 900$\n\n"
            "💬 AI-Чат-боти — Telegram, Instagram та сайти, які продають 24/7.\n"
            "💰 Ціна: від 400$ до 1100$\n\n"
            "📊 Аналітика — прогнозування продажів, аналіз даних, звіти.\n"
            "💰 Ціна: від 250$ до 600$\n\n"
            "📧 AI-Розсилки — автоматичні персоналізовані повідомлення.\n"
            "💰 Ціна: від 70$ до 300$\n\n"
            "🔍 AI-SEO Оптимізація — ключові слова, контент, технічна оптимізація.\n"
            "💰 Ціна: від 300$ до 1000$\n\n"
            "📝 Промпт-менеджер — професійні AI-промпти для маркетингу.\n"
            "💰 Ціна: від 100$ до 400$\n\n"
            "📞 Звʼяжіться з нами:\n"
            "Телефон: +380671902929\n"
            "Сайт: https://whitemedia.com.ua\n\n"
            "✅ Замовте консультацію вже сьогодні!",
            reply_markup=reply_markup
        )
        return

    if text == "📝 Промпт-менеджер":
        await update.message.reply_text(
            "📝 Ми створюємо професійні AI-промпти для маркетингу, реклами та контенту.\n"
            "Ваш бізнес отримує готові інструменти.",
            reply_markup=reply_markup
        )
        return

    # 📞 КОНТАКТИ
    if text == "📞 Звʼязатися з менеджером":
        await update.message.reply_text(
            "📞 Телефон: +380671902929\n🌐 Сайт: https://whitemedia.com.ua/\n\nЗвертайтесь для консультації!",
            reply_markup=reply_markup
        )
        return

    # 🤖 AI відповідь
    answer = ai_answer(text)
    add_request(user.id, "ask", text)
    await update.message.reply_text(answer, reply_markup=reply_markup)


# 🚀 Запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
