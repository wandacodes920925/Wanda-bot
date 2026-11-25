import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLAUDE_KEY = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Wanda! I'm live with Muse. Send me anything.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not CLAUDE_KEY:
        await update.message.reply_text(f"You said: {text} (Add CLAUDE_API_KEY in Render to get smart replies)")
        return
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": CLAUDE_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-3-5-sonnet-20241022", "max_tokens": 500, "messages": [{"role": "user", "content": text}]},
            timeout=30
        )
        data = r.json()
        reply = data["content"][0]["text"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot starting...")
    app.run_polling()
