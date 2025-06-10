import requests
import httpx
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import CallbackQueryHandler
import asyncio
from telegram import Bot
import re

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
    "برنامه نویس", "ساخت", "developer", "ساخته شده", "ساخته شدی"
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
    text = re.sub(r'[^\w\s]' , '' , text)
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
    await query.answer()  # برای حذف چرخش لودینگ روی دکمه

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

    # پاسخ‌های کلیدواژه‌ای
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

        if "choices" in res:
            reply = res["choices"][0]["message"]["content"]
        else:
            reply = "متاسفم، مشکلی در پاسخ‌دهی پیش آمد."
    except Exception as e:
        print("Error in API request: ", e)
        reply = "⚠️ مشکلی در اتصال به هوش مصنوعی پیش آمد."

    keyboard = [
        [InlineKeyboardButton("📩 تماس با توسعه‌دهنده", url="https://t.me/MNDEVV")],
        [InlineKeyboardButton("💡 راهنما", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(reply, reply_markup=reply_markup)

if __name__ == "__main__":
    async def main():
        bot = Bot(BOT_TOKEN)
        await bot.delete_webhook()  # 🔥 حذف وب‌هوک برای جلوگیری از Conflict

        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("reset", reset))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(CallbackQueryHandler(button_callback))
        await app.run_polling()

    asyncio.run(main())