import os
import random
import difflib
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

# 🔑 Bot Token Railway variable se aayega
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔴 YAHAN APNA DATABASE CHANNEL USERNAME DALO (without @)
DATABASE_CHANNEL = "filmy_database"

# 🧠 Insaan jaisi baat
SMALL_TALK = [
    "Haan bhai 😊",
    "Bol bhai kya chahiye?",
    "Admin online hai 😎",
    "Movie ka naam likh bhai 🎬",
    "Aaj kya dekhna hai?"
]

MOVIE_FOUND = [
    "Le bhai mil gayi 🔥",
    "Ye rahi bhai movie 😍",
    "Full HD file hai bhai 😎",
    "Enjoy kar bhai 🎬"
]

MOVIE_NOT_FOUND = [
    "Bhai thodi der me upload kar raha hoon ⏳",
    "Server pe aa rahi hai bhai, wait karo 🔄",
    "Aaj hi daal dunga bhai 👍",
    "Link process me hai bhai 😌"
]

def correct_spelling(text, titles):
    match = difflib.get_close_matches(text, titles, n=1, cutoff=0.6)
    return match[0] if match else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Admin Online Hai\nMovie ka naam likho bhai 🎬"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    movie_posts = []
    movie_titles = []

    async for msg in context.bot.get_chat_history(
        chat_id=DATABASE_CHANNEL,
        limit=200
    ):
        if msg.text:
            movie_posts.append(msg.text)
            movie_titles.append(msg.text.lower())

    # 🔍 Direct match
    for post in movie_posts:
        if user_text in post.lower():
            reply = random.choice(MOVIE_FOUND)
            await update.message.reply_text(
                f"{reply}\n\n🎬 {post}\n\nKaisi lagi bhai? 😁"
            )
            return

    # 🔁 Spelling correction
    corrected = correct_spelling(user_text, movie_titles)
    if corrected:
        for post in movie_posts:
            if corrected in post.lower():
                await update.message.reply_text(
                    f"Samajh gaya bhai 😄\n\n🎬 {post}\n\nEnjoy kar ❤️"
                )
                return

    # 💬 Movie nahi mili → admin style reply
    if len(user_text.split()) >= 2:
        await update.message.reply_text(random.choice(MOVIE_NOT_FOUND))
    else:
        await update.message.reply_text(random.choice(SMALL_TALK))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 AI Admin Movie Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
