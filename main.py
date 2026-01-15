from telethon import TelegramClient, events
import os

api_id = int(os.environ["31114489"])
api_hash = os.environ["990fc1c611ce074d3fb5b694fb88702c"]
bot_token = os.environ["8110394902:AAHWQPCZMDWLOdzR5Q0c1J-76-UZsQyFz-M"]

source_channel = os.environ["https://t.me/hcmbd"]
target_channel = os.environ["https://t.me/hcmdail"]

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    await client.send_message(target_channel, event.message)

client.run_until_disconnected()