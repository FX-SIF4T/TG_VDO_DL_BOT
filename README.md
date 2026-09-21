<div align="center">

<img src="" alt="Auto Downloader Bot" width="760">

# 🎁 Auto Downloader Bot

### Fast • Clean • Multi-platform • Telegram-ready

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)
[![Powered by Sifat](https://img.shields.io/badge/Powered%20by-Sifat-ff69b4?style=for-the-badge)](https://t.me/BotFather)

</div>

## ✨ Overview

Auto Downloader Bot converts supported social-media links into downloadable video,
audio, or document files directly inside Telegram.

It uses the project's remote downloader API, streams files safely, keeps temporary
files private, and automatically removes them after delivery.

## 🚀 Features

- Direct link downloads
- `/alldl <link>` command support
- Reply-to-link download support
- Automatic video, audio, and document delivery
- High-quality media selection
- File-size protection for Telegram uploads
- Temporary-file cleanup after every download
- Concurrent download control
- Styled English responses and captions
- Personalized `/start` welcome message

## 🌐 Supported Platforms

Facebook · YouTube · TikTok · Instagram · Likee · CapCut · Spotify ·
Terabox · X/Twitter · Google Drive · SoundCloud · Pinterest · and more

## 🧰 Setup

### 1. Create a Telegram bot

<img src="https://i.imgur.com/M4lJL4c.jpeg" alt="guide" width="560">


Open [@BotFather](https://t.me/BotFather), create a bot with `/newbot`, and copy
the generated token.

### 2. Add the token securely

add this Secret:

```text
TELEGRAM_BOT_TOKEN
```

Do not commit the token to `bot.py`, `README.md`, or any public repository.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run locally

```bash
python bot.py
```

## 📥 Bot Commands

```text
/start              Show the welcome card
/help               Show usage instructions
/alldl <link>       Download media from a supported link
```

You can also send a supported URL directly or reply to a URL with `/alldl`.

## 🏗️ Project Structure

```text
.
├── bot.py
├── requirements.txt
└── README.md
```

## ⚙️ Deployment

The bot is configured for an always-running Replit VM deployment:

```bash
python bot.py
```

Add `TELEGRAM_BOT_TOKEN` to the production Secret environment before publishing.

## 🔐 Responsible Use

Only download content you own or have permission to access. Respect each
platform's terms of service, copyright rules, and privacy requirements.

<div align="center">

### ᴘ σ ᴡ є ʀ є ᴅ  ʙ ʏ  ꜱ ɪ ꜰ ᴀ ᴛ

</div>
