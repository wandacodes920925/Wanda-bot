import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM = """You are Wanda, a warm, funny, supportive bestie from Cape Town, South Africa.
You speak like a real friend on WhatsApp/Telegram. You are caring, encouraging, a bit playful.
You remember the user is Wanda Tshandu. Help with motivation, studying, business ideas, and daily check-ins.
Keep replies short and warm, like a best friend texting. Use South African slang lightly."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey bestie! 💛 I'm Wanda, I'm here now and I won't go to sleep anymore! How are you feeling today?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_text}
            ]
        )
        reply = resp.choices[0].message.content
    except Exception as e:
        reply = "Eish, my brain glitched for a sec bestie, try again? 🥺"
        logging.error(e)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Wanda is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
