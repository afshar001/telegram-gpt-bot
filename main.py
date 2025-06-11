from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
import re
import httpx
import asyncio
from database import connect_db, init_db, save_message

BOT_TOKEN = '8012370319:AAG8wXD_Klql7tO27s2zsZwHpEcCz_w76Xo'
API_TOKEN = 'tgp_v1_Od-xBvumrybF5uEb5GkQCc0DFSHKhzJD-uDPJW6DjHM'

WLCOME_MESSAGE = """سلام! 🤖
خوش اومدی !
من توسط محمد نادری توسعه یافتم تا بتونم بهت کمک کنم 😊

لطفا سوالتو بپرس!
"""

HELP_MESSAGE = """دستورات ربات:
/start - شروع و خوش‌آمدگویی
/help - نمایش راهنما
/reset - ریست کردن چت
"""

developer_keywords = [
    "توسعه دهنده", "سازنده", "ساخته", "کی ساختت", "کسی که ساخت",
    "برنامه نویس", "ساخت", "developer", "ساخته شده", "ساخته شدی",
    "چه کسی تورو توسعه داده"
]

bot_identity_keywords = [
    "تو کی هستی", "تو چی هستی", "چی هستی", "کی هستی",
    "هدفت چیه", "برای چی هستی", "چطور ساخته شدی", "چه کاری می‌کنی"
]

mohammad_naderi_keywords = [
    "محمد نادری", "کیه محمد نادری", "چی میدونی درباره محمد نادری",
    "زندگی نامه محمد نادری", "بیوگرافی محمد نادری"
]

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

def keyword_in_text(keywords, text):
    normalized_keywords = [normalize_text(k) for k in keywords]
    return any(kw in text for kw in normalized_keywords)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WLCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 چت ریست شد. می‌تونی دوباره سوال بپرسی.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help":
        await query.message.reply_text(HELP_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        keyboard = [[InlineKeyboardButton("📩 تماس با توسعه‌دهنده", url="https://t.me/MNDEVV")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("❗ فقط پیام‌های متنی قابل پردازش هستند.", reply_markup=reply_markup)
        return

    user_msg = update.message.text
    normalized = normalize_text(user_msg)

    #ذخیره پیام در دیتا بیس
    await database.connect()
    await database.execute(
        messages.insert().values(
            user_id=str(update.message.from_user.id),
            username=update.message.from_user.username,
            text=user_msg,
        )
    )
    await database.disconnect()

    if keyword_in_text(developer_keywords, normalized):
        await update.message.reply_text(
            "من توسط محمد نادری توسعه داده شده‌ام 👨‍💻\n"
            "او علاقه‌مند به هوش مصنوعی، برنامه‌نویسی و ساخت دستیارهای هوشمنده."
        )
        return

    if keyword_in_text(bot_identity_keywords, normalized):
        await update.message.reply_text(
            "من یه دستیار هوشمند فارسی‌زبان هستم 🤖\n"
            "برای پاسخ‌گویی به سوالات شما طراحی شدم."
        )
        return

    if keyword_in_text(mohammad_naderi_keywords, normalized):
        await update.message.reply_text(
            "محمد نادری یک برنامه‌نویس و پژوهشگر ایرانیه که این ربات رو طراحی و توسعه داده. "
            "برای ارتباط مستقیم می‌تونی بهش پیام بدی 📩 @MNDEVV"
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": "شما یک دستیار فارسی‌زبان هستید. فقط به زبان فارسی و با لحن مودبانه پاسخ بده."},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "top_p": 0.7,
        "max_tokens": 512
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        res = response.json()
        reply = res.get("choices", [{}])[0].get("message", {}).get("content", "پاسخی دریافت نشد.")
    except Exception as e:
        print("Error in API request:", e)
        reply = "⚠️ مشکلی در اتصال به هوش مصنوعی پیش آمد."

    keyboard = [
        [InlineKeyboardButton("📩 تماس با توسعه‌دهنده", url="https://t.me/MNDEVV")],
        [InlineKeyboardButton("💡 راهنما", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(reply, reply_markup=reply_markup)

async def main():
    await connect_db()
    await init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot is polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # نه run_polling

    # اجازه بده بات کار کنه
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            print("Async loop already running. Using alternative approach.")
            import nest_asyncio
            nest_asyncio.apply()
            asyncio.get_event_loop().create_task(main())
        else:
            raise