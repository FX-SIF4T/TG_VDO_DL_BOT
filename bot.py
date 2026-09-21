from __future__ import annotations

import asyncio
import json
import logging
import mimetypes
import os
import re
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import aiohttp
from telegram import InputFile, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_TELEGRAM_BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("media-downloader-bot")

STYLE_MAP = str.maketrans({
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ",
    "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ",
    "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ",
    "s": "ꜱ", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x",
    "y": "ʏ", "z": "ᴢ",
    "A": "ᴀ", "B": "ʙ", "C": "ᴄ", "D": "ᴅ", "E": "ᴇ", "F": "ꜰ",
    "G": "ɢ", "H": "ʜ", "I": "ɪ", "J": "ᴊ", "K": "ᴋ", "L": "ʟ",
    "M": "ᴍ", "N": "ɴ", "O": "ᴏ", "P": "ᴘ", "Q": "ǫ", "R": "ʀ",
    "S": "ꜱ", "T": "ᴛ", "U": "ᴜ", "V": "ᴠ", "W": "ᴡ", "X": "x",
    "Y": "ʏ", "Z": "ᴢ",
})


def styled(value: object) -> str:
    return str(value).translate(STYLE_MAP)


def welcome_text(name: str, members: object) -> str:
    return (
        "╭── [ 🎁 ᴡ є ʟ ᴄ σ ϻ є  ʙ ᴧ ʙ ʏ 🎁 ]\n"
        "│\n"
        f"├── 🍼 ⇛ η ᴧ ϻ є : {styled(name)}\n"
        f"├── 🩷 ⇛ ϻ є ϻ ʙ є ʀ s : {styled(members)}\n"
        "│\n"
        "├── 🎁 ⇛ єηᴊσʏ ᴛʜє ϻυsɪᴄ ᴧηᴅ ᴠɪᴅ !\n"
        "│\n"
        "╰── ᴘ σ ᴡ є ʀ є ᴅ  ʙ ʏ  ꜱɪꜰᴀᴛ"
    )


def help_text() -> str:
    return (
        "╭── [ 🎀 ᴅ ᴏ ᴡ ɴ ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ɢ ᴜ ɪ ᴅ ᴇ 🎀 ]\n"
        "│\n"
        "├── 📥 ⇛ /alldl <ʟɪɴᴋ>\n"
        "├── 🔗 ⇛ ꜱᴇɴᴅ ᴀ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ ᴅɪʀᴇᴄᴛʟʏ\n"
        "├── 💬 ⇛ ʀᴇᴘʟʏ ᴛᴏ ᴀ ʟɪɴᴋ ᴡɪᴛʜ /alldl\n"
        "│\n"
        "├── 🌐 ⇛ ꜰᴀᴄᴇʙᴏᴏᴋ • ʏᴏᴜᴛᴜʙᴇ • ᴛɪᴋᴛᴏᴋ\n"
        "├── 🌐 ⇛ ɪɴꜱᴛᴀɢʀᴀᴍ • ʟɪᴋᴇᴇ • ᴄᴀᴘᴄᴜᴛ\n"
        "├── 🌐 ⇛ ꜱᴘᴏᴛɪꜰʏ • ᴛᴇʀᴀʙᴏx • x • ᴘɪɴᴛᴇʀᴇꜱᴛ\n"
        "│\n"
        "╰── ᴘ σ ᴡ є ʀ є ᴅ  ʙ ʏ  ꜱɪꜰᴀᴛ"
    )


RAW_API_CONFIG_URL = (
    "https://raw.githubusercontent.com/FX-SIF4T/API-STORE/"
    "refs/heads/main/FXS_APIS/apis.json"
)

SUPPORTED_DOMAINS = {
    "facebook.com",
    "fb.watch",
    "youtube.com",
    "youtu.be",
    "tiktok.com",
    "instagram.com",
    "instagr.am",
    "likee.com",
    "likee.video",
    "capcut.com",
    "spotify.com",
    "terabox.com",
    "twitter.com",
    "x.com",
    "drive.google.com",
    "soundcloud.com",
    "ndown.app",
    "pinterest.com",
    "pin.it",
}

MAX_DOWNLOAD_BYTES = 49 * 1024 * 1024
MAX_CONCURRENT_DOWNLOADS = 3
URL_PATTERN = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
TRAILING_URL_CHARS = ".,!?;:'\""

DOWNLOAD_SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)


class DownloaderError(Exception):
    pass


def extract_url(text: str | None) -> str | None:
    if not text:
        return None

    match = URL_PATTERN.search(text)
    if not match:
        return None

    return match.group(0).rstrip(TRAILING_URL_CHARS)


def is_supported_url(url: str) -> bool:
    try:
        hostname = (urlparse(url).hostname or "").lower().removeprefix("www.")
    except ValueError:
        return False

    return any(hostname == domain or hostname.endswith(f".{domain}")
               for domain in SUPPORTED_DOMAINS)


def platform_name(url: str) -> str:
    hostname = (urlparse(url).hostname or "media").lower()
    hostname = hostname.removeprefix("www.")
    return hostname.split(".")[0].upper()


def safe_filename(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^\w .-]+", "_", value, flags=re.UNICODE).strip(" .")
    return (cleaned[:80] or fallback).strip()


def choose_extension(media_url: str, content_type: str | None = None) -> str:
    path_suffix = Path(urlparse(media_url).path).suffix.lower()
    allowed = {
        ".mp3", ".m4a", ".aac", ".ogg", ".wav",
        ".mp4", ".mkv", ".webm", ".mov", ".avi",
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
    }
    if path_suffix in allowed:
        return path_suffix

    guessed = mimetypes.guess_extension((content_type or "").split(";")[0])
    if guessed in allowed:
        return guessed

    return ".mp4"


def first_media_url(payload: Any) -> str | None:
    if isinstance(payload, dict):
        for key in ("high_quality", "low_quality", "url", "downloadUrl", "download_url"):
            value = payload.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value

        for key in ("data", "result", "media"):
            nested = first_media_url(payload.get(key))
            if nested:
                return nested

    if isinstance(payload, list):
        for item in payload:
            nested = first_media_url(item)
            if nested:
                return nested

    return None


def payload_title(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None

    for key in ("title", "filename", "file_name", "name"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


async def response_json(response: aiohttp.ClientResponse) -> Any:
    raw_text = await response.text()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise DownloaderError(styled("The downloader API returned invalid data.")) from exc


async def get_downloader_base(session: aiohttp.ClientSession) -> str:
    try:
        async with session.get(RAW_API_CONFIG_URL) as response:
            response.raise_for_status()
            config = await response_json(response)
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        raise DownloaderError(styled("The downloader API is currently unavailable.")) from exc

    if not isinstance(config, dict):
        raise DownloaderError(styled("The downloader configuration is invalid."))

    base_url = config.get("downloadere") or config.get("downloader")
    if not isinstance(base_url, str) or not base_url.startswith(("http://", "https://")):
        raise DownloaderError(styled("The downloader endpoint was not found."))

    return base_url.rstrip("/")


async def resolve_media(session: aiohttp.ClientSession, source_url: str) -> tuple[str, Any]:
    downloader_base = await get_downloader_base(session)
    endpoint = f"{downloader_base}/alldl"

    try:
        async with session.get(endpoint, params={"url": source_url}) as response:
            response.raise_for_status()
            payload = await response_json(response)
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        raise DownloaderError(styled("The media request failed. Please try again.")) from exc

    media_url = first_media_url(payload)
    if not media_url:
        raise DownloaderError(styled("No downloadable media was found for this link."))

    return media_url, payload


async def download_to_file(
    session: aiohttp.ClientSession,
    media_url: str,
) -> tuple[str, str]:
    try:
        async with session.get(media_url) as response:
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            announced_size = response.content_length
            if announced_size and announced_size > MAX_DOWNLOAD_BYTES:
                raise DownloaderError(styled("This file is larger than Telegram's upload limit."))

            extension = choose_extension(media_url, content_type)
            temporary_file = tempfile.NamedTemporaryFile(
                prefix="telegram_media_",
                suffix=extension,
                delete=False,
            )
            temporary_path = temporary_file.name

            downloaded = 0
            try:
                with temporary_file:
                    async for chunk in response.content.iter_chunked(64 * 1024):
                        downloaded += len(chunk)
                        if downloaded > MAX_DOWNLOAD_BYTES:
                            raise DownloaderError(styled("This file is larger than Telegram's upload limit."))
                        temporary_file.write(chunk)
            except Exception:
                Path(temporary_path).unlink(missing_ok=True)
                raise

            return temporary_path, extension
    except DownloaderError:
        raise
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        raise DownloaderError(styled("The media file could not be downloaded."))


def message_url(update: Update) -> str | None:
    message = update.effective_message
    if not message:
        return None

    url = extract_url(message.text or message.caption)
    if url:
        return url

    replied = message.reply_to_message
    if replied:
        return extract_url(replied.text or replied.caption)

    return None


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(help_text())


async def show_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message:
        return

    user = update.effective_user
    name = user.first_name if user and user.first_name else "Guest"
    try:
        members = await context.bot.get_chat_member_count(message.chat_id)
    except Exception:
        members = "—"

    await message.reply_text(welcome_text(name, members))


async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message:
        return

    url = message_url(update)
    if not url and context.args:
        url = extract_url(" ".join(context.args))

    if not url:
        if message.text and message.text.startswith("/"):
            await message.reply_text(styled("📥 Please send a complete https:// media link."))
        return

    if not is_supported_url(url):
        await message.reply_text(styled("❌ This platform is not supported."))
        return

    session: aiohttp.ClientSession = context.application.bot_data["http_session"]
    status_message = await message.reply_text(
        styled("⏳ Checking your link and preparing the media...")
    )
    temporary_path: str | None = None

    async with DOWNLOAD_SEMAPHORE:
        try:
            await context.bot.send_chat_action(
                chat_id=message.chat_id,
                action=ChatAction.UPLOAD_VIDEO,
            )
            media_url, payload = await resolve_media(session, url)
            temporary_path, extension = await download_to_file(session, media_url)

            title = safe_filename(
                payload_title(payload) or f"{platform_name(url)}_media",
                "downloaded_media",
            )
            filename = f"{title}{extension}"
            caption = (
                "╭── [ 🎁 ᴅ ᴏ ᴡ ɴ ʟ ᴏ ᴀ ᴅ  ᴄ ᴏ ᴍ ᴘ ʟ ᴇ ᴛ ᴇ 🎁 ]\n"
                "│\n"
                f"├── 🌐 ⇛ ᴘ ʟ ᴀ ᴛ ꜰ ᴏ ʀ ᴍ : {styled(platform_name(url))}\n"
                "├── ✅ ⇛ ꜱ ᴛ ᴀ ᴛ ᴜ ꜱ : ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ\n"
                "│\n"
                "├── ✨ ⇛ ᴇ ɴ ᴊ ᴏ ʏ ʏ ᴏ ᴜ ʀ ᴍ ᴇ ᴅ ɪ ᴀ !\n"
                "│\n"
                "╰── ᴘ σ ᴡ є ʀ є ᴅ  ʙ ʏ  ꜱ ɪ ꜰ ᴀ ᴛ"
            )

            await status_message.edit_text(
                styled("📤 Media found. Uploading it to Telegram...")
            )
            if extension in {".mp3", ".m4a", ".aac", ".ogg", ".wav"}:
                with open(temporary_path, "rb") as media_file:
                    await message.reply_audio(
                        audio=InputFile(media_file, filename=filename),
                        caption=caption,
                    )
            elif extension in {".mp4", ".webm", ".mov"}:
                with open(temporary_path, "rb") as media_file:
                    await message.reply_video(
                        video=InputFile(media_file, filename=filename),
                        caption=caption,
                        supports_streaming=True,
                    )
            else:
                with open(temporary_path, "rb") as media_file:
                    await message.reply_document(
                        document=InputFile(media_file, filename=filename),
                        caption=caption,
                    )

            await status_message.delete()
        except DownloaderError as exc:
            await status_message.edit_text(f"❌ {exc}")
        except Exception:
            logger.exception("Unexpected download error")
            await status_message.edit_text(
                styled("❌ Something went wrong. Please try again later.")
            )
        finally:
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)


async def post_init(application: Application) -> None:
    timeout = aiohttp.ClientTimeout(total=120, connect=20, sock_read=120)
    application.bot_data["http_session"] = aiohttp.ClientSession(timeout=timeout)


async def post_shutdown(application: Application) -> None:
    session: aiohttp.ClientSession | None = application.bot_data.get("http_session")
    if session and not session.closed:
        await session.close()


def build_application(token: str) -> Application:
    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    application.add_handler(CommandHandler("start", show_welcome))
    application.add_handler(CommandHandler("help", show_help))
    application.add_handler(CommandHandler("alldl", download_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_handler)
    )
    return application


def main() -> None:
    token = BOT_TOKEN
    if not token or token == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise SystemExit(
            "Add your Telegram bot token to BOT_TOKEN or set "
            "the TELEGRAM_BOT_TOKEN environment variable."
        )

    application = build_application(token)
    logger.info("Telegram downloader bot is starting")
    application.run_polling()


if __name__ == "__main__":
    main()
