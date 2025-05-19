import telegram
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")

async def handle_message(update, context):
    url = update.message.text
    if "youtube.com" not in url:
        await update.message.reply_text("Please send a valid YouTube link.")
        return

    await update.message.reply_text("Checking for copyright...")

    response = requests.post(BACKEND_URL, json={"url": url})
    data = response.json()
    if data["status"] == "rejected":
        await update.message.reply_text(f"Upload blocked: {data['message']}")
    elif data["status"] == "success":
        await update.message.reply_text(f"Uploaded: {data['message']}")
    else:
        await update.message.reply_text("Something went wrong.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()
