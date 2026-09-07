import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8923052745:AAHRZ2Z9FT_l9WhEA4M3d5FoOpP7S__FP8w"
SESSION_STRING = "AQIeqDwAkvb9zKIDScNpDqUkS3PntZlnDVWD2e5xi38Gt08slAb6iB9Y1VSx3P8TVl1dwTil9_kTypoww4puVGWv6CNRFZN9GgUu3mANVfIyQR0gyoroykRn1ymx9ZAYwkg_7qGZWjA4aXy2QUI7_cThIyADTh9_AQQhckP-z1N4e5bqBgufh1aZ6HCYpAFtHC62w8Mr5QHZJNiFbJwmc1UQhtubSHesPOXb_SsIFPk3tFbujJrBiw4iB_q1Z6SVJXh0iLZ7xIKboBjjJ0KthrOOMiATER3FmtvB0IJ_jC73jx2RJbxRmJ84f_zXrz2gbb5Kz5u7ZQwRGBb9-TgR0MjG3z9vOQAAAAIKSphPAA"
# Tested high-speed live stream link
STREAM_URL = "http://stream.zeno.fm/f3wvbbqmdg8uv"

bot = Client("RuvikaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RuvikaAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user)

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("🎧 Ruvika VC Bot is Active!\nUse `/play` in group to start streaming.")

@bot.on_message(filters.command("play"))
async def play_handler(client, message):
    chat_id = message.chat.id
    m = await message.reply_text("🔄 Connecting & Playing Audio...")
    try:
        await call_py.play(
            chat_id,
            MediaStream(
                STREAM_URL,
                audio_parameters=MediaStream.AudioParameters(
                    bitrate=48000
                )
            )
        )
        await m.edit_text("🎶 **Live Music playing in Voice Chat now!** 📻")
    except Exception as e:
        print(f"Play Error: {e}", flush=True)
        await m.edit_text(f"Error: {e}")

@bot.on_message(filters.command("stop"))
async def stop_handler(client, message):
    try:
        await call_py.leave_call(message.chat.id)
        await message.reply_text("⏹️ Stream band kar di gayi hai.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

async def start_services():
    await user.start()
    await call_py.start()
    print(">>> USER & PYTGCALLS STARTED <<<", flush=True)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_services())
    print(">>> BOT RUNNING <<<", flush=True)
    bot.run()
