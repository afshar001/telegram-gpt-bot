import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN ='7641748037:AAEO5DpbHpR25cgGwWssXbXvFLLY8amTbQQ'
API_TOKEN = 'tgp_v1_Od-xBvumrybF5uEb5GkQCc0DFSHKhzJD-uDPJW6DjHM'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! سوالت رو بپرس 😊")

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

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
    res = response.json()

    if "choices" in res:
        reply = res["choices"][0]["message"]["content"]
    else:
        reply = "متاسفم، مشکلی در پاسخ‌دهی پیش آمد."

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()