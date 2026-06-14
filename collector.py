import feedparser
import requests
from bs4 import BeautifulSoup
import logging
from config import RSS_FEEDS, KEYWORDS

def fetch_rss_feeds():
    """Fetches articles from configured RSS feeds."""
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # Basic fields
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')
                
                # Source
                source = feed.feed.get('title', feed_url)

                # Filter by keywords
                if is_relevant(title, summary):
                    # For some feeds, we might need to fetch the full page to get better content
                    content = extract_article_content(link, summary)
                    
                    # Basic structure
                    articles.append({
                        'title': title,
                        'url': link,
                        'source': source,
                        'content': content
                    })
        except Exception as e:
            logging.error(f"Error fetching feed {feed_url}: {e}")
            
    return articles

def is_relevant(title: str, summary: str) -> bool:
    """Checks if the article contains any of the target keywords."""
    combined_text = f"{title} {summary}".lower()
    for keyword in KEYWORDS:
        if keyword.lower() in combined_text:
            return True
    return False

def extract_article_content(url: str, default_summary: str) -> str:
    """Attempts to extract the main content using BeautifulSoup."""
    # Basic attempt, if it fails, fallback to RSS summary
    try:
        # A simple request with a standard user-agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract paragraphs
            paragraphs = soup.find_all('p')
            text_content = ' '.join([p.get_text() for p in paragraphs])
            
            # If we got reasonable text, return it (limit to ~2000 chars to avoid huge payloads)
            if len(text_content) > 100:
                return text_content[:2000]
    except Exception as e:
        logging.debug(f"Failed to extract content from {url}: {e}")
        
    # Fallback to the summary from the RSS feed (stripping HTML tags)
    soup = BeautifulSoup(default_summary, 'html.parser')
    return soup.get_text()[:2000]
