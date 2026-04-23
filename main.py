# NaijaGPT - by Elias Banda
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# STEP 1: REPLACE THIS WITH YOUR REAL TOKEN FROM BOTFATHER
TOKEN = "8797262651:AAES8B-y2VcPtefUuvax_9awb36s6bvCKhk"

# STEP 2: 
pidgin_replies = {
    "how far": "I dey o Chief, you good? 😎",
    "wetin dey": "Na code dey sup o. You dey grind WAEC? 📚",
    "you don chop": "I don chop semicolon chop bug 😂 You?",
    "abeg": "No worry Chief, I dey for you 💪"
}

# STEP 3: what happens when user type /start, /help, etc

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How far Chief! Na NaijaGPT be this 🤖\n\n"
        "I sabi small pidgin. Try: 'how far' or use /help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "NaijaGPT Commands:\n\n"
        "/start - Begin yarn\n"
        "/help - Show this message\n"
        "/about - Who build me\n\n"
        "Or just chat: 'how far', 'wetin dey'"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "NaijaGPT V0.2 🇳🇬\n"
        "Built by Elias Banda\n"
        "AFIT Accounting student learning Python\n"
        "Day 2 of coding. Meta loading... 💪"
    )

# STEP 4: This handles normal messages like "how far"
async def reply_pidgin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.lower()
    
    if user_msg in pidgin_replies:
        await update.message.reply_text(pidgin_replies[user_msg])
    else:
        await update.message.reply_text("Omo I no grab that one yet o 😅 Try /help")
import json
import os

# Load saved pidgin words when bot start
def load_pidgin_dict():
    if os.path.exists("pidgin_words.json"):
        with open("pidgin_words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save new word to file
def save_pidgin_dict(pidgin_dict):
    with open("pidgin_words.json", "w", encoding="utf-8") as f:
        json.dump(pidgin_dict, f, ensure_ascii=False, indent=2)

# Load am once when bot start
CUSTOM_PIDGIN = load_pidgin_dict()

async def addword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = " ".join(context.args) # Join all words after /addword
        if "=" not in text:
            await update.message.reply_text("Format wrong o 😅 Use am like this:\n`/addword shakara = forming`")
            return
        
        word, meaning = text.split("=", 1)
        word = word.strip().lower()
        meaning = meaning.strip()
        
        CUSTOM_PIDGIN[word] = meaning
        save_pidgin_dict(CUSTOM_PIDGIN)
        
        await update.message.reply_text(f"Sharp! I don learn am 💚\n\n**{word}** = {meaning}")
    except:
        await update.message.reply_text("Wahala! Use am like this:\n`/addword word = meaning`")

async def listwords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CUSTOM_PIDGIN:
        await update.message.reply_text("Nobody don teach me new words yet o 😭 Use /addword to teach me")
        return
    
    words = "\n".join([f"• **{w}** = {m}" for w, m in CUSTOM_PIDGIN.items()])
    await update.message.reply_text(f"Words wey una don teach me:\n\n{words}")
# STEP 5: Connect everything together
app = ApplicationBuilder().token(TOKEN).build()

# Register commands - VERY IMPORTANT
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_pidgin))
async def howfar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I dey o my paddy! 😎 You sef how you dey? Body still dey inside cloth?")

async def wahala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wahala no dey finish o 😂 But we go dey alright las. Wetin sup?")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    jokes = [
        "Why NEPA no dey go comedy show? Because their light no dey bright 😂",
        "My guy go gym once. Now e dey tell everybody say 'I be fitness coach' 🤣",
        "Danfo driver: 'You go pay abi I go use you do sacrifice?' 😭"
    ]
    await update.message.reply_text(random.choice(jokes))

# Register the new commands - ADD THESE WITH THE OTHERS
app.add_handler(CommandHandler("howfar", howfar))
app.add_handler(CommandHandler("wahala", wahala))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("addword", addword))
app.add_handler(CommandHandler("listwords", listwords))

print("NaijaGPT dey online o... Press Ctrl+C to stop")
app.run_polling()  # 👈 THIS ONE, NOT bot.polling()
