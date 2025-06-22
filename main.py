import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
FORCE_CHANNELS = os.environ.get("FORCE_CHANNELS", "@channel1 @channel2").split()

bot = Client("force_sub_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def is_user_joined_all_channels(bot, user_id):
    for channel in FORCE_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except:
            return False
    return True

@bot.on_message(filters.group & filters.new_chat_members)
async def new_member_handler(client, message):
    for user in message.new_chat_members:
        if not await is_user_joined_all_channels(client, user.id):
            await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions())
            buttons = [[InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{ch[1:]}")]
                       for ch in FORCE_CHANNELS]
            buttons.append([InlineKeyboardButton("🔁 I've Joined All", callback_data="check_join")])
            await message.reply(
                f"👋 Hey {user.mention}!\n🚫 Join all required channels to chat here.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

@bot.on_callback_query(filters.regex("check_join"))
async def recheck_callback(client, callback_query):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    if await is_user_joined_all_channels(client, user_id):
        await client.unrestrict_chat_member(chat_id, user_id)
        await callback_query.message.edit_text("✅ You're now unmuted. Welcome!")
    else:
        await callback_query.answer("❗ Still not joined all channels!", show_alert=True)

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    channels_list = "\n".join([f"- {ch}" for ch in FORCE_CHANNELS])
    await message.reply(
        "🤖 I'm a Force-Subscribe Bot.\nJoin these channels before you can chat in your group:\n" + channels_list
    )

@bot.on_message(filters.command("clone") & filters.private)
async def clone_handler(client, message):
    repo_url = "https://github.com/STD-DEEPANSHU/force"  # Replace with your GitHub repo
    deploy_url = f"https://heroku.com/deploy?template={repo_url}"
    await message.reply(
        "🚀 **Make Your Own Bot!**\nClick to deploy your own bot like me.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 Deploy to Heroku", url=deploy_url)]]
        )
    )

bot.run()
