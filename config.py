import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

# Settings
MAX_POSTS_PER_DAY = int(os.getenv("MAX_POSTS_PER_DAY", 5))
TIMEZONE = "Asia/Kolkata"

# Content Filtering
KEYWORDS = [
    "coin", "numismatic", "heritage", "ancient", 
    "archaeology", "mint", "currency", "medallion"
]

# RSS Feeds to scrape
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=numismatics+OR+%22ancient+coins%22+OR+archaeology+India",
    "http://numismatics.org/feed/",
    "https://www.coinworld.com/rss",
    "https://blog.britishmuseum.org/category/coins-and-medals/feed/",
    "https://www.reddit.com/r/coins/.rss",
    "https://www.reddit.com/r/numismatics/.rss"
]
