<div align="center">
  
# 🎁 Auto Downloader Bot

### Fast • Clean • Multi-platform • Telegram-ready

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)
[![Powered by Sifat](https://img.shields.io/badge/Powered%20by-Sifat-ff69b4?style=for-the-badge)](https://t.me/BotFather)

## ✨ Overview

Auto Downloader Bot converts supported social-media links into downloadable video,
audio, or document files directly inside Telegram.

It uses the VDL Linklet API for video downloads and search, streams files safely,
keeps temporary files private, and automatically removes them after delivery.

## 🚀 Features

- Direct link downloads
- `/alldl <link>` command support
- `/search <query>` video search with up to five numbered results
- Send or reply with a result number to download that video
- Reply-to-link download support
- Automatic video, audio, and document delivery
- File-size protection for Telegram uploads
- Temporary-file cleanup after every download
- Concurrent download control

## 🌐 Supported Platforms

Facebook · YouTube · TikTok · Instagram · Likee · CapCut · Spotify ·
Terabox · X/Twitter · Google Drive · SoundCloud · Pinterest · and more

## 🧰 Setup

### 1. Create a Telegram bot

<img src="https://i.imgur.com/M4lJL4c.jpeg" alt="guide" width="560">
------
<img src="https://i.imgur.com/r4sJGIU.jpeg" alt="guide" width="560">

Open [@BotFather](https://t.me/BotFather), create a bot with `/newbot`, and copy
the generated token.

### 2. Add the token securely

Set the `TELEGRAM_BOT_TOKEN` secret. Do not commit the token to the repository.

### 3. Install dependencies and run

```bash
pip install -r requirements.txt
python bot.py
```

## 📥 Bot Commands

```text
/start              Show the welcome card
/help               Show usage instructions
/alldl <link>       Download media from a supported link
/search <query>     Search videos and show up to five numbered results
```

After searching, send a result number (1–5) in the same chat—or reply to the
search results message with that number—to download the selected video. You can
also send a supported URL directly or reply to a URL with `/alldl`.

## 🏗️ Project Structure

```text
.
bot.py
requirements.txt
README.md
```

## ⚙️ Deployment

This bot runs on [Render](https://render.com/) as a **Background Worker**.

```text
Build Command: pip install -r requirements.txt
Start Command: python bot.py
```

Set `TELEGRAM_BOT_TOKEN` in the deployment environment. No public port is
required because the bot uses Telegram polling.

## 🔐 Responsible Use

Only download content you own or have permission to access. Respect each
platform's terms of service, copyright rules, and privacy requirements.

</div>

<div align="center">

### ᴘ σ ᴡ є ʀ є ᴅ  ʙ ʏ  ꜱ ɪ ꜰ ᴀ ᴛ

</div>
