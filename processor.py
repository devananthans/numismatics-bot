import requests
from bs4 import BeautifulSoup
import logging

KEYWORD_HASHTAG_MAP = {
    "coin": "#Coins #Numismatics",
    "india": "#IndianHeritage #India",
    "ancient": "#AncientHistory",
    "gold": "#GoldCoin",
    "silver": "#SilverCoin",
    "mughal": "#MughalEra",
    "gupta": "#GuptaEmpire",
    "chola": "#CholaEmpire #தமிழ்நாடு",
    "roman": "#RomanCoins",
    "museum": "#Museum #Heritage",
    "archaeology": "#Archaeology"
}

def extract_summary(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs[:3]])
        if not text.strip():
            return ""
        return text[:400]
    except Exception as e:
        logging.error(f"Error extracting summary from {url}: {e}")
        return ""

def generate_hashtags(text):
    tags = set(["#Numismatics", "#Heritage", "#நாணயவரலாறு"])
    text_lower = text.lower()
    for keyword, hashtag in KEYWORD_HASHTAG_MAP.items():
        if keyword in text_lower:
            for tag in hashtag.split():
                tags.add(tag)
    return " ".join(tags)

def format_post(title, summary, link, source):
    hashtags = generate_hashtags(title + " " + summary)
    post = f"""
🪙 இன்றைய நாணய வரலாறு | Today's Coin History

🏛️ {title}

📖 {summary}...

🔗 மேலும் படிக்க: {link}
📰 Source: {source}

{hashtags}
"""
    return post.strip()
