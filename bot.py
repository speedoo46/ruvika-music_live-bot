import os
import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

# Direct Telegram Credentials
API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8253242144:AAGrX7Hs3e7l3sN5D2K0UPfA6VGmX10uSZk"
SESSION_STRING = "AQIeqDwAkvb9zKIDScNpDqUkS3PntZlnDVWD2e5xi38Gt08slAb6iB9Y1VSx3P8TVl1dwTil9_kTypoww4puVGWv6CNRFZN9GgUu3mANVfIyQR0gyoroykRn1ymx9ZAYwkg_7qGZWjA4aXy2QUI7_cThIyADTh9_AQQhckP-z1N4e5bqBgufh1aZ6HCYpAFtHC62w8Mr5QHZJNiFbJwmc1UQhtubSHesPOXb_SsIFPk3tFbujJrBiw4iB_q1Z6SVJXh0iLZ7xIKboBjjJ0KthrOOMiATER3FmtvB0IJ_jC73jx2RJbxRmJ84f_zXrz2gbb5Kz5u7ZQwRGBb9-TgR0MjG3z9vOQAAAAIKSphPAA"
@bot.on_message(filters.command(["start", "start@ruvika_music_bot"]))
async def start_cmd(client, message):
    print(f"[CMD] Start from {message.from_user.id}", flush=True)
    await message.reply_text(
        "🎧 **Ruvika 24/7 VC Music Bot is Active!** 🎧\n\n"
        "Commands:\n"
        "• `/play` - Group Voice Chat me live streaming shuru karein\n"
        "• `/stop` - Voice Chat stream band karein"
    )

@bot.on_message(filters.command(["play", "play@ruvika_music_bot"]))
async def play_vc(client, message):
    chat_id = message.chat.id
    print(f"[CMD] Play requested in chat: {chat_id}", flush=True)
    status = await message.reply_text("🔄 Connecting to Voice Chat...")
    try:
        await call_py.play(chat_id, MediaStream(STREAM_URL))
        await status.edit_text("🎶 **24/7 Music is now LIVE in Voice Chat!** 📻\nNon-stop radio chal raha hai.")
    except Exception as e:
        print(f"[ERROR] Play: {e}", flush=True)
        await status.edit_text(f"⚠️ Error: `{str(e)}`")

@bot.on_message(filters.command(["stop", "stop@ruvika_music_bot"]))
async def stop_vc(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_call(chat_id)
        await message.reply_text("⏹️ Voice Chat stream band kar di gayi hai.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`")

async def main():
    print("Starting Bot Client...", flush=True)
    await bot.start()
    print("Starting Assistant...", flush=True)
    await user.start()
    print("Starting PyTgCalls...", flush=True)
    await call_py.start()
    print(">>> RUVIKA 24/7 VC BOT IS READY & LISTENING! <<<", flush=True)
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
