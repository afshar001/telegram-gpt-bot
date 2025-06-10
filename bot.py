import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot import WLCOME_MESSAGE

BOT_TOKEN ='8012370319:AAG8wXD_Klql7tO27s2zsZwHpEcCz_w76Xo'
API_TOKEN = 'tgp_v1_Od-xBvumrybF5uEb5GkQCc0DFSHKhzJD-uDPJW6DjHM'

WLCOME_MESSAGE = """سلام! 🤖
خوش اومدی !\n من توسط محمد نادری توسعه یافتم تا بتونم بهت کمک کنم
\n
لطفا سوالتو بپرس !!
"""
HELP_MESSAGE = """دستورات ربات:
/start - شروع و خوش‌آمدگویی
/help - نمایش راهنما
/reset - ریست کردن چت
"""

#فرمان استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WLCOME_MESSAGE)

#فرمان help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)

#فرمان ریست )نمادین فعلا
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 چت ریست شد. می‌تونی دوباره سوال بپرسی.")

# دریافت و پاسخ به پیام‌ها    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "top_p": 0.7,
        "max_tokens": 512
    }
    try:
        
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        res = response.json()

        if "choices" in res:
            reply = res["choices"][0]["message"]["content"]
        else:
            reply = "متاسفم، مشکلی در پاسخ‌دهی پیش آمد."
    except Exception as e :
         reply = "⚠️ مشکلی در اتصال به هوش مصنوعی پیش آمد."

    keyboard = [
        [InlineKeyboardButton("📩 تماس با توسعه‌دهنده", url="https://t.me/MNDEVV")]
    ]
    reply_markup = InlineKeyboardButton(keyboard)
    await update.message.reply_text(reply , reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
