import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# -----------------------------
# Environment Variables
# -----------------------------
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL", "")
TARGET_CHANNEL = os.environ.get("TARGET_CHANNEL", "")
PORT = int(os.environ.get("PORT", 10000))  # For Render free-tier web service

# -----------------------------
# Flask Web Server (Keep Alive)
# -----------------------------
app = Flask(name)

@app.route("/")
def home():
    return "Telegram Forwarder Bot is running ✅"

# -----------------------------
# Telegram Bot Logic
# -----------------------------
def start_telegram_bot():
    """Initialize and run the Telegram bot"""
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(chats=SOURCE_CHANNEL))
    async def forward_message(event):
        """Forward every new message from source to target channel"""
        try:
            await client.send_message(TARGET_CHANNEL, event.message)
        except Exception as e:
            print(f"[ERROR] Failed to forward message: {e}")

    print("[INFO] Telegram bot is running...")
    client.run_until_disconnected()

# -----------------------------
# Main Entry Point
# -----------------------------
if name == "main":
    # Run Telegram bot in a separate thread
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()

    # Run Flask web server (required for Render free-tier)
    print(f"[INFO] Starting Flask server on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)
