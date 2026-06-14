# Numismatics & Heritage Content Aggregator Telegram Bot

This is a complete, production-ready Python project that fetches news about numismatics, ancient coins, and heritage from various RSS feeds, processes them to extract key information using Beautiful Soup, and posts them to a Telegram group/channel.

## Features
- Scrapes 6+ RSS feeds and filters based on keywords
- SQLite database to prevent duplicate posts and auto-cleanup old entries
- Free scraping and summary extraction using BeautifulSoup and RSS feeds
- Formats posts beautifully with emojis
- Posts updates automatically at scheduled times (9 AM, 6 PM daily, and a weekly digest on Sunday 10 AM)
- Rate limits to a maximum of 5 posts per day

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Telegram Bot Token and Group/Channel ID

### 2. Installation
Clone the repository (or navigate to the project folder) and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
1. Rename `.env.example` to `.env`.
2. Fill in the required API keys and configuration values in the `.env` file:
   - `TELEGRAM_BOT_TOKEN`: The token you get from BotFather.
   - `TELEGRAM_GROUP_ID`: The ID of your Telegram channel/group (e.g., `-1001234567890`).

### 4. Running the Bot
To start the bot and its scheduler, run:
```bash
python main.py
```
This will start a blocking process that waits for the scheduled times to execute the tasks. Check `bot_log.txt` for real-time logs and debug information.
