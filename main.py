# Don't Remove Credit Tg - @newstudent1885
# Ask Doubt on telegram @newstudent1885

import os
import re
import sys
import json
import time
import m3u8
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import datetime
import random
import ffmpeg
import logging
import yt_dlp

from subprocess import getstatusoutput
from aiohttp import web, ClientSession
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl

import core as helper
from core import *
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN

from pyromod import listen
from pytube import YouTube, Playlist

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"


async def show_random_emojis(message: Message):
    emojis = [
        '🎊','🔮','😎','⚡️','🚀','✨','💥','🎉',
        '🥂','🍾','🦠','🤖','❤️‍🔥','🕊️','💃','🥳','🐅','🦁'
    ]
    emoji_message = await message.reply_text(
        ' '.join(random.choices(emojis, k=1))
    )
    return emoji_message


# OWNER
OWNER_ID = 5840594311

# SUDO USERS
SUDO_USERS = [5840594311]

# AUTH CHANNELS
AUTH_CHANNELS = [
    -1002605113558,
    -1002663510614
]


def is_authorized(user_id: int) -> bool:
    return (
        user_id == OWNER_ID
        or user_id in SUDO_USERS
        or user_id in AUTH_CHANNELS
    )


bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
# ================== SUDO COMMAND ==================

@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        await message.reply_text("🚫 You are not authorized to use this command.")
        return

    try:
        args = message.text.split(" ", 2)

        if len(args) < 3:
            await message.reply_text("Usage:\n/sudo add <user_id>\n/sudo remove <user_id>")
            return

        action = args[1].lower()
        target_user_id = int(args[2])

        if action == "add":

            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"✅ User {target_user_id} added to sudo list.")
            else:
                await message.reply_text("⚠️ User already in sudo list.")

        elif action == "remove":

            if target_user_id == OWNER_ID:
                await message.reply_text("🚫 Owner cannot be removed.")
                return

            if target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"✅ User {target_user_id} removed.")
            else:
                await message.reply_text("⚠️ User not found.")

        else:
            await message.reply_text("Usage:\n/sudo add <user_id>\n/sudo remove <user_id>")

    except Exception as e:
        await message.reply_text(f"Error: {e}")


# ================== START COMMAND ==================

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "🇮🇳 BOT MADE BY 🇮🇳",
                url="https://t.me/newstudent1885"
            )
        ],
        [
            InlineKeyboardButton(
                "🔔 UPDATE CHANNEL 🔔",
                url="https://t.me/+dXRSrF1762o5NmRl"
            )
        ],
        [
            InlineKeyboardButton(
                "🦋 FOLLOW US 🦋",
                url="https://t.me/+-fFQMVMRwMU4ZDBl"
            )
        ]
    ]
)

image_urls = [
    "https://graph.org/file/996e7252ff3ffc679b3ea-ffc78c21ecf8396f98.jpg",
    "https://graph.org/file/439c62c6244b05050c93b-f02497c99181cdead5.jpg"
]

random_image_url = random.choice(image_urls)

caption = (
    "**Hello 👋**\n\n"
    "➠ I am TXT to Video Uploader Bot\n"
    "➠ Send /tushar to start upload\n"
    "➠ Send /help for commands"
)


@bot.on_message(filters.command("start"))
async def start_command(bot: Client, message: Message):

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )


# ================== HELP COMMAND ==================

@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg: Message):

    help_text = (
        "/start - Start bot\n\n"
        "/tushar - Upload TXT links\n\n"
        "/restart - Restart bot\n\n"
        "/stop - Stop process\n\n"
        "/cookies - Upload cookies\n\n"
        "/e2t - Edit txt\n\n"
        "/yt2txt - Extract playlist\n\n"
        "/sudo add/remove - Manage sudo\n\n"
        "/userlist - Show sudo users"
    )

    await msg.reply_text(help_text)
    # ================== RESTART & STOP ==================

@bot.on_message(filters.command("stop"))
async def stop_command(_, m: Message):
    await m.reply_text("🛑 Bot Stopped")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("restart"))
async def restart_command(_, m: Message):

    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized.")
        return

    await m.reply_text("🔄 Restarting Bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)


# ================== USER LIST ==================

@bot.on_message(filters.command("userlist"))
async def list_users(client: Client, msg: Message):

    if msg.from_user.id != OWNER_ID:
        return

    if not SUDO_USERS:
        await msg.reply_text("No sudo users.")
        return

    text = "\n".join([f"User ID: `{u}`" for u in SUDO_USERS])
    await msg.reply_text(f"SUDO USERS:\n\n{text}")


# ================== COOKIES COMMAND ==================

COOKIES_FILE_PATH = "youtube_cookies.txt"


@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):

    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized.")
        return

    await m.reply_text("📂 Send cookies file (.txt)")

    try:
        input_message: Message = await client.listen(m.chat.id)

        if not input_message.document:
            await m.reply_text("❌ Send .txt file only.")
            return

        if not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("❌ Only .txt cookies allowed.")
            return

        downloaded_path = await input_message.download()

        with open(downloaded_path, "r") as uploaded:
            cookies_content = uploaded.read()

        with open(COOKIES_FILE_PATH, "w") as target:
            target.write(cookies_content)

        await input_message.reply_text("✅ Cookies Updated Successfully")

    except Exception as e:
        await m.reply_text(f"Error: {e}")


# ================== TXT EDITOR ==================

os.makedirs("downloads", exist_ok=True)

UPLOAD_FOLDER = "downloads"


@bot.on_message(filters.command("e2t"))
async def edit_txt(client: Client, message: Message):

    await message.reply_text(
        "📂 Send TXT file containing titles and links"
    )

    input_message: Message = await client.listen(message.chat.id)

    if not input_message.document:
        await message.reply_text("❌ Send valid TXT file.")
        return

    file_name = input_message.document.file_name.lower()

    uploaded_path = os.path.join(UPLOAD_FOLDER, file_name)

    await input_message.download(uploaded_path)

    await message.reply_text(
        "Send new filename or type `d` for default"
    )

    user_response: Message = await client.listen(message.chat.id)

    if user_response.text.lower() == "d":
        final_name = file_name
    else:
        final_name = user_response.text + ".txt"

    try:

        with open(uploaded_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        subjects = {}
        current = None

        for line in lines:

            line = line.strip()

            if ":" in line:

                title, url = line.split(":", 1)

                title = title.strip()
                url = url.strip()

                if title not in subjects:
                    subjects[title] = {"links": [], "topics": []}

                subjects[title]["links"].append(url)
                current = title

            elif line.startswith("-") and current:
                subjects[current]["topics"].append(
                    line.replace("-", "").strip()
                )

        sorted_subjects = sorted(subjects.items())

        output_path = os.path.join(UPLOAD_FOLDER, final_name)

        with open(output_path, "w", encoding="utf-8") as f:

            for title, data in sorted_subjects:

                for link in data["links"]:
                    f.write(f"{title}:{link}\n")

                for topic in sorted(data["topics"]):
                    f.write(f"- {topic}\n")

        await message.reply_document(
            output_path,
            caption="✅ TXT Edited Successfully"
        )

    except Exception as e:
        await message.reply_text(f"Error: {e}")
        # ================== YT PLAYLIST → TXT ==================

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')


def get_videos_with_ytdlp(url):

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    try:

        with YoutubeDL(ydl_opts) as ydl:

            result = ydl.extract_info(url, download=False)

            if "entries" in result:

                title = result.get("title", "playlist")

                videos = {}

                for entry in result["entries"]:

                    video_url = entry.get("url")
                    video_title = entry.get("title")

                    if video_url:

                        if not video_title:
                            video_title = "video"

                        videos[video_title] = video_url

                return title, videos

        return None, None

    except Exception as e:

        logging.error(f"YT extract error: {e}")

        return None, None


def save_to_file(videos, name):

    filename = f"{sanitize_filename(name)}.txt"

    with open(filename, "w", encoding="utf-8") as f:

        for title, url in videos.items():

            f.write(f"{title}: {url}\n")

    return filename


@bot.on_message(filters.command("yt2txt"))
async def ytplaylist_to_txt(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:

        await message.reply_text(
            "🚫 Only owner can use this command."
        )

        return

    await message.delete()

    ask = await message.reply_text(
        "📥 Send YouTube Playlist URL"
    )

    input_msg = await client.listen(ask.chat.id)

    yt_url = input_msg.text

    await input_msg.delete()

    await ask.delete()

    title, videos = get_videos_with_ytdlp(yt_url)

    if not videos:

        await message.reply_text(
            "❌ Could not extract playlist."
        )

        return

    file_name = save_to_file(videos, title)

    await message.reply_document(
        file_name,
        caption=f"📥 Extracted playlist\n\n{title}"
    )

    os.remove(file_name)
    # ================== MAIN TXT UPLOADER ==================

@bot.on_message(filters.command(["tushar"]))
async def upload(bot: Client, m: Message):

    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized to use this bot.")
        return

    editable = await m.reply_text("📂 Send TXT file containing links")

    input_msg: Message = await bot.listen(editable.chat.id)

    file_path = await input_msg.download()

    await input_msg.delete()

    try:

        with open(file_path, "r") as f:
            lines = f.read().splitlines()

    except Exception:
        await m.reply_text("❌ Invalid TXT file")
        return

    links = []

    for line in lines:

        if "://" in line:

            parts = line.split("://", 1)

            links.append(parts)

    if not links:

        await m.reply_text("❌ No links found in file")
        return

    await editable.edit(
        f"🔗 Total Links Found: {len(links)}\n\nStarting download..."
    )

    count = 1
    failed = 0

    for item in links:

        try:

            name = item[0].replace(":", "").strip()

            url = "https://" + item[1]

            filename = f"{str(count).zfill(3)}_{name[:40]}"

            cmd = f'yt-dlp -o "{filename}.mp4" "{url}"'

            subprocess.run(cmd, shell=True)

            if os.path.exists(f"{filename}.mp4"):

                await bot.send_video(
                    m.chat.id,
                    f"{filename}.mp4",
                    caption=f"🎬 {filename}"
                )

                os.remove(f"{filename}.mp4")

            count += 1

        except Exception:

            failed += 1

            continue

    await m.reply_text(
        f"""✅ Batch Completed

Total Links: {len(links)}
Failed: {failed}
Successful: {len(links)-failed}"""
    )


# ================== BOT START ==================

print("🚀 Bot Started Successfully")

bot.run()
