import os
import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

REQUIRED_BOTS = os.environ.get("REQUIRED_BOTS", "").split()  # Example: "@bot1 @bot2"
BOT_KEYS = [bot.replace("@", "") for bot in REQUIRED_BOTS]

DB_FILE = "db.json"

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = str(message.from_user.id)
    db = load_db()

    not_joined = []
    for bot_key in BOT_KEYS:
        if bot_key not in db or user_id not in db[bot_key]:
            not_joined.append(bot_key)

    if not not_joined:
        await message.reply("🎉 Access granted! You have started all required bots.")
    else:
        buttons = [
            [InlineKeyboardButton(f"Start @{bot}", url=f"https://t.me/{bot}")]
            for bot in not_joined
        ]
        buttons.append([InlineKeyboardButton("🔁 I’ve Started All", callback_data="check")])
        await message.reply(
            "⚠️ You must start these bots first:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@app.on_callback_query(filters.regex("check"))
async def recheck(client, callback_query):
    user_id = str(callback_query.from_user.id)
    db = load_db()

    not_joined = []
    for bot_key in BOT_KEYS:
        if bot_key not in db or user_id not in db[bot_key]:
            not_joined.append(bot_key)

    if not not_joined:
        await callback_query.message.edit("✅ All checks passed! Welcome.")
    else:
        await callback_query.answer("❌ You still haven't started all bots.", show_alert=True)

app.run()
