import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import os
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Fake website so Render sees a port
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

JOKES = [
    "Why did the chicken cross the road? To get to the other side... and to avoid load shedding 😂",
    "What do you call a fish without eyes? A fsh!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What did the ocean say to the beach? Nothing, it just waved!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call cheese that isn't yours? Nacho cheese!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey Wanda! 👋 I'm back!\n\n"
        "I'm your Telegram bot from Cape Town 🇿🇦\n\n"
        "Try these:\n"
        "/joke - I'll tell you a joke\n"
        "/whoami - Who are you?\n"
        "/help - All commands\n\n"
        "Or just chat to me!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here's what I can do Wanda:\n"
        "/start - Say hi\n"
        "/joke - Random joke\n"
        "/whoami - Your info\n"
        "/help - This list"
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You are Wanda Tshandu ✨\n"
        "From Cape Town, South Africa 🇿🇦\n"
        "And you are awesome!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "hi" in text or "hello" in text or "hey" in text:
        await update.message.reply_text("Hey Wanda! 👋 How are you doing today?")
    elif "joke" in text:
        await update.message.reply_text(random.choice(JOKES))
    elif "who are you" in text or "your name" in text:
        await update.message.reply_text("I'm your Telegram bot! Made just for you, Wanda 💛")
    elif "how are you" in text:
        await update.message.reply_text("I'm good! Living my best life in the cloud ☁️ How are you?")
    elif "bye" in text:
        await update.message.reply_text("Bye Wanda! Come back soon 👋")
    elif "cape town" in text:
        await update.message.reply_text("Cape Town! Best city in the world 🇿🇦 Table Mountain and all!")
    else:
        await update.message.reply_text(f"Interesting, Wanda! You said: '{update.message.text}' 😄 Tell me more?")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()
