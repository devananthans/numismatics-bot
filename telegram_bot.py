import asyncio
from telegram import Bot
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID

def send_telegram_message_sync(text: str):
    """Synchronous wrapper to send a telegram message."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_telegram_bot_token_here':
        logging.error("Telegram bot token is not configured.")
        return False
        
    try:
        # python-telegram-bot v20 uses async functions
        asyncio.run(_send_telegram_message_async(text))
        return True
    except Exception as e:
        logging.error(f"Failed to send telegram message: {e}")
        return False

async def _send_telegram_message_async(text: str, max_retries=3):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for attempt in range(max_retries):
        try:
            await bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=text,
                disable_web_page_preview=False
            )
            logging.info("Message sent successfully to Telegram.")
            return
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed to send message: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                logging.error("Max retries reached. Message delivery failed.")
                raise e
