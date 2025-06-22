from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from config import API_ID, API_HASH, BOT_TOKEN

DB_FILE = "db.json"
REQUIRED_BOTS = os.environ.get("REQUIRED_BOTS", "").split()
BOT_KEYS = [bot.replace("@", "") for bot in REQUIRED_BOTS]

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        return json.load(f)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = str(message.from_user.id)
    db = load_db()
    not_done = [bot for bot in BOT_KEYS if user_id not in db.get(bot, [])]

    if not not_done:
        await message.reply("✅ All required bots have been started! You're good to go.")
    else:
        buttons = [
            [InlineKeyboardButton(f"Start @{bot}", url=f"https://t.me/{bot}?start=check")]
            for bot in not_done
        ]
        buttons.append([InlineKeyboardButton("🔁 I've Started All", callback_data="check_all")])
        await message.reply(
            "👋 To continue, please start all the required bots below:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@app.on_callback_query(filters.regex("check_all"))
async def check_all(client, callback_query):
    user_id = str(callback_query.from_user.id)
    db = load_db()
    not_done = [bot for bot in BOT_KEYS if user_id not in db.get(bot, [])]

    if not not_done:
        await callback_query.message.edit("✅ You’ve started all bots! Access granted.")
    else:
        await callback_query.answer("❌ Some bots are still missing. Start them and tap again.", show_alert=True)

@app.on_message(filters.command("clone") & filters.private)
async def clone_cmd(client, message):
    repo_url = "https://github.com/STD-DEEPANSHU/force"  # 🔁 replace with your repo
    deploy_url = f"https://heroku.com/deploy?template={repo_url}"
    await message.reply(
        "**🚀 Want to Create Your Own System?**\n\n"
        "1. Get a new bot token from @BotFather.\n"
        "2. Click below to deploy your own version.\n"
        "3. Set ENV vars: `API_ID`, `API_HASH`, `BOT_TOKEN`, `BOT_ID`, `REQUIRED_BOTS`\n\n"
        "Your `BOT_ID` should be your bot's username (without @).",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 Deploy to Heroku", url=deploy_url)]]
        )
    )

app.run()
