import os
import telebot
import google.generativeai as genai
from collections import defaultdict

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Store conversation history per user
user_histories = defaultdict(list)
user_profiles = {}

SYSTEM_PROMPT = """
You are a thoughtful, helpful assistant.
You are warm, intelligent and a bit playful.
Keep answers short and useful for mobile chat.
"""

def ask_gemini(user_id, user_message):
    history = user_histories[user_id]
    history.append({"role": "user", "parts": [user_message]})
    # Keep last 10 messages to avoid getting too long
    history = history[-10:]
    user_histories[user_id] = history

    chat = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Got it, I'll be helpful and concise."]},
        *history[:-1]
    ])
    response = chat.send_message(user_message)
    reply = response.text
    user_histories[user_id].append({"role": "model", "parts": [reply]})
    return reply

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! I'm your assistant. Ask me anything. Use /whoami to set up your profile, /reset to clear our chat.")

@bot.message_handler(commands=['whoami'])
def whoami(message):
    bot.reply_to(message, "Tell me about yourself - what's your name, what do you do, what do you like? I'll remember it.")
    user_profiles[message.from_user.id] = "awaiting"

@bot.message_handler(commands=['reset'])
def reset(message):
    user_histories[message.from_user.id] = []
    bot.reply_to(message, "Cleared! Fresh start.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if user_profiles.get(user_id) == "awaiting":
        user_profiles[user_id] = text
        bot.reply_to(message, f"Got it, thanks! I'll remember that.")
        return

    try:
        reply = ask_gemini(user_id, text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Sorry, something went wrong: {e}")

print("Bot is running...")
bot.infinity_polling()
