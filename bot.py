import os
import asyncio
from pyrogram import Client, filters, compose
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8923052745:AAHRZ2Z9FT_l9WhEA4M3d5FoOpP7S__FP8w"
SESSION_STRING = "AQIeqDwAkvb9zKIDScNpDqUkS3PntZlnDVWD2e5xi38Gt08slAb6iB9Y1VSx3P8TVl1dwTil9_kTypoww4puVGWv6CNRFZN9GgUu3mANVfIyQR0gyoroykRn1ymx9ZAYwkg_7qGZWjA4aXy2QUI7_cThIyADTh9_AQQhckP-z1N4e5bqBgufh1aZ6HCYpAFtHC62w8Mr5QHZJNiFbJwmc1UQhtubSHesPOXb_SsIFPk3tFbujJrBiw4iB_q1Z6SVJXh0iLZ7xIKboBjjJ0KthrOOMiATER3FmtvB0IJ_jC73jx2RJbxRmJ84f_zXrz2gbb5Kz5u7ZQwRGBb9-TgR0MjG3z9vOQAAAAIKSphPAA"
STREAM_URL = "https://radioindia.net/radio/mirchi98/icecast.audio"

bot = Client("RuvikaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RuvikaAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True)
call_py = PyTgCalls(user)

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    print(f"Received start command from {message.from_user.id}", flush=True)
    await message.reply_text(
        "🎧 **Ruvika 24/7 VC Music Bot is Online!** 🎧\n\n"
        "Commands:\n"
        "• `/play` - Group VC me live streaming chalu karein\n"
        "• `/stop` - VC stream band karein"
    )

@bot.on_message(filters.command("play"))
async def play_handler(client, message):
    chat_id = message.chat.id
    status = await message.reply_text("🔄 Connecting to Voice Chat...")
    try:
        await call_py.play(chat_id, MediaStream(STREAM_URL))
        await status.edit_text("🎶 **24/7 Music is now LIVE in Voice Chat!** 📻")
    except Exception as e:
        await status.edit_text(f"⚠️ Error: `{str(e)}`")

@bot.on_message(filters.command("stop"))
async def stop_handler(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
        await message.reply_text("⏹️ Voice Chat stream band kar di gayi hai.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`")

async def main():
    # Dono accounts ko start karein
    await bot.start()
    await user.start()
    await call_py.start()
    print(">>> RUVIKA 24/7 VC BOT IS FULLY ONLINE & READY! <<<", flush=True)
    
    # Telegram update polling loop active rakhein
    await idle()
    
    # Graceful shutdown
    await call_py.stop()
    await user.stop()
    await bot.stop()

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
