import os
import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8253242144:AAGrX7Hs3e7l3sN5D2K0UPfA6VGmX10uSZk"
SESSION_STRING = "AQIeqDwAkvb9zKIDScNpDqUkS3PntZlnDVWD2e5xi38Gt08slAb6iB9Y1VSx3P8TVl1dwTil9_kTypoww4puVGWv6CNRFZN9GgUu3mANVfIyQR0gyoroykRn1ymx9ZAYwkg_7qGZWjA4aXy2QUI7_cThIyADTh9_AQQhckP-z1N4e5bqBgufh1aZ6HCYpAFtHC62w8Mr5QHZJNiFbJwmc1UQhtubSHesPOXb_SsIFPk3tFbujJrBiw4iB_q1Z6SVJXh0iLZ7xIKboBjjJ0KthrOOMiATER3FmtvB0IJ_jC73jx2RJbxRmJ84f_zXrz2gbb5Kz5u7ZQwRGBb9-TgR0MjG3z9vOQAAAAIKSphPAA"
STREAM_URL = "https://radioindia.net/radio/mirchi98/icecast.audio"

bot = Client("RuvikaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RuvikaAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True)
call_py = PyTgCalls(user)

# Har message ko print karne ke liye (Debug)
@bot.on_message()
async def all_incoming(client, message):
    text = message.text or ""
    print(f">> Incoming update: {text} from {message.chat.id}", flush=True)
    
    if text.startswith("/start"):
        await message.reply_text(
            "🎧 **Ruvika 24/7 VC Music Bot is Active!** 🎧\n\n"
            "Commands:\n"
            "• `/play` - Group Voice Chat me live streaming shuru karein\n"
            "• `/stop` - Voice Chat stream band karein"
        )
    elif text.startswith("/play"):
        status = await message.reply_text("🔄 Connecting to Voice Chat...")
        try:
            await call_py.play(message.chat.id, MediaStream(STREAM_URL))
            await status.edit_text("🎶 **24/7 Music is now LIVE in Voice Chat!** 📻\nRadio stream chalu hai!")
        except Exception as e:
            print(f">> VC Error: {e}", flush=True)
            await status.edit_text(f"⚠️ VC Error: `{str(e)}`")
    elif text.startswith("/stop"):
        try:
            await call_py.leave_call(message.chat.id)
            await message.reply_text("⏹️ Voice Chat band kar di gayi hai.")
        except Exception as e:
            await message.reply_text(f"⚠️ Error: `{str(e)}`")

async def run_bot():
    print("Connecting Clients...", flush=True)
    await bot.start()
    await user.start()
    await call_py.start()
    print(">>> BOT FULLY ACTIVE & WAITING FOR COMMANDS <<<", flush=True)
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
