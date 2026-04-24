import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx
from threading import Thread
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "NaijaGPT Bot is running!"

TOKEN = os.environ.get("TOKEN")
print(f"BOT STARTING... TOKEN = {TOKEN}")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Omo! NaijaGPT dey here. How far?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}"}
    data = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_msg}]}
    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = r.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    print(f"FLASK STARTING ON PORT {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    time.sleep(2) # Give Flask 2 seconds to bind port first
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("TELEGRAM POLLING STARTED...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    run_bot()
