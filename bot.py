import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import MediaStream

# Direct Telegram Credentials
API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8253242144:AAGrX7Hs3e7l3sN5D2K0UPfA6VGmX10uSZk"
SESSION_STRING = os.getenv("SESSION_STRING", "")

# 24/7 Live Stream Audio URL
STREAM_URL = os.getenv("STREAM_URL", "https://radioindia.net/radio/mirchi98/icecast.audio")

bot = Client("RuvikaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RuvikaAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user)

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🎧 **Ruvika 24/7 VC Music Bot is Active!** 🎧\n\n"
        "Commands:\n"
        "• `/play` - Group Voice Chat me live music start karein\n"
        "• `/stop` - Voice Chat leave karein"
    )

@bot.on_message(filters.command("play") & (filters.group | filters.channel))
async def play_vc(client, message):
    chat_id = message.chat.id
    status = await message.reply_text("🔄 Joining Voice Chat...")
    
    try:
        await call_py.play(
            chat_id,
            MediaStream(STREAM_URL)
        )
        await status.edit_text("🎶 **24/7 Music is now LIVE in Voice Chat!** 📻\nStream successfully chal rahi hai.")
    except Exception as e:
        await status.edit_text(f"⚠️ Error: `{str(e)}`\n\n(Dhyan rahe: Voice Chat active honi chahiye aur Assistant group me add hona chahiye).")

@bot.on_message(filters.command("stop") & (filters.group | filters.channel))
async def stop_vc(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
        await message.reply_text("⏹️ Voice Chat stream band kar di gayi hai.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`")

async def start_services():
    await bot.start()
    await user.start()
    await call_py.start()
    print("Ruivika 24/7 VC Bot is Online!")
    await idle()

if __name__ == "__main__":
    asyncio.run(start_services())
