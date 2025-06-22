from pyrogram import Client, filters
import os
import json
from config import API_ID, API_HASH, BOT_TOKEN

BOT_ID = os.environ.get("BOT_ID")  # Important: must match what’s in REQUIRED_BOTS in main bot
DB_FILE = "db.json"

app = Client(BOT_ID, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

@app.on_message(filters.command("start") & filters.private)
async def mark_user_started(client, message):
    user_id = str(message.from_user.id)
    db = load_db()
    
    if BOT_ID not in db:
        db[BOT_ID] = []
    
    if user_id not in db[BOT_ID]:
        db[BOT_ID].append(user_id)
        save_db(db)
        await message.reply("✅ You’ve started this bot! You can now go back to the main bot.")
    else:
        await message.reply("👋 You’ve already started me. You're good to go!")

app.run()
