from telethon import TelegramClient, events
from flask import Flask
import threading
import os
name = "punk"
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

source_channel = os.environ["SOURCE_CHANNEL"]
target_channel = os.environ["TARGET_CHANNEL"]

app = Flask(name)

@app.route("/")
def home():
    return "Bot is running"

def run_bot():
    client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        await client.send_message(target_channel, event.message)

    client.run_until_disconnected()

if name == "main":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


