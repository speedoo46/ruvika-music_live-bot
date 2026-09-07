import os
import asyncio
import requests
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = 35563580
API_HASH = "8603427418daa03b4d6a69ef493e6872"
BOT_TOKEN = "8923052745:AAHRZ2Z9FT_l9WhEA4M3d5FoOpP7S__FP8w"
SESSION_STRING = "AQIeqDwAkvb9zKIDScNpDqUkS3PntZlnDVWD2e5xi38Gt08slAb6iB9Y1VSx3P8TVl1dwTil9_kTypoww4puVGWv6CNRFZN9GgUu3mANVfIyQR0gyoroykRn1ymx9ZAYwkg_7qGZWjA4aXy2QUI7_cThIyADTh9_AQQhckP-z1N4e5bqBgufh1aZ6HCYpAFtHC62w8Mr5QHZJNiFbJwmc1UQhtubSHesPOXb_SsIFPk3tFbujJrBiw4iB_q1Z6SVJXh0iLZ7xIKboBjjJ0KthrOOMiATER3FmtvB0IJ_jC73jx2RJbxRmJ84f_zXrz2gbb5Kz5u7ZQwRGBb9-TgR0MjG3z9vOQAAAAIKSphPAA"
RADIO_URL = "http://stream.zeno.fm/f3wvbbqmdg8uv"
API_BASE_URL = "https://jiosavanapiryden.vercel.app/api"

bot = Client("RuvikaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RuvikaAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user)

def get_song_url(query):
    try:
        url = f"{API_BASE_URL}/search/songs"
        res = requests.get(url, params={"query": query, "page": 0, "limit": 1}, timeout=10)
        data = res.json()
        if data.get("success") and data.get("data", {}).get("results"):
            song = data["data"]["results"][0]
            song_id = song.get("id")
            
            # Details API
            detail_res = requests.get(f"{API_BASE_URL}/songs/{song_id}", timeout=10).json()
            if detail_res.get("success") and detail_res.get("data"):
                links = detail_res["data"][0].get("downloadUrl", [])
                if links:
                    return links[-1].get("url"), song.get("name", "Song")
    except Exception as e:
        print(f"Fetch error: {e}", flush=True)
    return None, None

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        "🎧 **Ruvika VC Music Bot Online!**\n\n"
        "• `/play` - 24/7 Live Radio stream\n"
        "• `/play <song name>` - JioSaavn se koi bhi song VC me chalayein\n"
        "• `/stop` - Stream band karein"
    )

@bot.on_message(filters.command("play"))
async def play_handler(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    status = await message.reply_text("🔄 Processing...")

    play_url = RADIO_URL
    song_name = "24/7 Live Radio"

    if query:
        await status.edit_text(f"🔍 Searching: `{query}`...")
        found_url, title = get_song_url(query)
        if found_url:
            play_url = found_url
            song_name = title
        else:
            await status.edit_text("❌ Gaana nahi mila! Radio play kar rahe hain...")

    try:
        # MediaStream ka standard direct initialization bina kisi extra class ke
        await call_py.play(chat_id, MediaStream(play_url))
        await status.edit_text(f"🎶 **Playing:** `{song_name}` in Voice Chat! 📻")
    except Exception as e:
        print(f"Play Error: {e}", flush=True)
        await status.edit_text(f"Error: `{e}`")

@bot.on_message(filters.command("stop"))
async def stop_handler(client, message):
    try:
        await call_py.leave_call(message.chat.id)
        await message.reply_text("⏹️ Voice chat stream band kar di gayi.")
    except Exception as e:
        await message.reply_text(f"Error: `{e}`")

async def start_services():
    await user.start()
    await call_py.start()
    print(">>> USER & PYTGCALLS STARTED <<<", flush=True)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_services())
    print(">>> BOT READY <<<", flush=True)
    bot.run()
