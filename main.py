import logging
import sys

from database import init_db, is_duplicate, mark_as_posted, cleanup_old_entries, get_weekly_stats
from collector import fetch_rss_feeds
from processor import extract_summary, format_post
from formatter import format_weekly_digest
from telegram_bot import send_telegram_message_sync

# Configure logging
logging.basicConfig(
    filename='bot_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def run_daily_job():
    logging.info("Starting daily job to fetch and post numismatic news.")
    
    init_db()
    
    articles = fetch_rss_feeds()
    if not articles:
        logging.info("No relevant articles found.")
        return

    posted_this_run = 0
    for article in articles:
        url = article['url']
        if is_duplicate(url):
            continue

        logging.info(f"Processing new article: {article['title']}")
        
        summary = article.get('content', '')
        if not summary or len(summary) < 50:
            summary = extract_summary(url)
            
        if not summary:
            summary = "Summary not available."
            
        summary = summary[:400]
        
        post_text = format_post(article['title'], summary, url, article['source'])
        success = send_telegram_message_sync(post_text)
        
        if success:
            mark_as_posted(url, article['title'], article['source'])
            posted_this_run += 1
            logging.info(f"Successfully posted article. Total this run: {posted_this_run}")
                
        # Limit to 3 posts per job run as requested in "Daily top 3 numismatic news posts"
        if posted_this_run >= 3:
            logging.info("Max posts per run reached. Stopping.")
            break

def run_weekly_digest():
    logging.info("Starting weekly digest job.")
    init_db()
    count, sources = get_weekly_stats()
    
    articles = fetch_rss_feeds()
    
    digest_text = format_weekly_digest(articles, count, sources)
    send_telegram_message_sync(digest_text)
    logging.info("Weekly digest posted.")

def run_cleanup_job():
    init_db()
    cleanup_old_entries(days=30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [daily|weekly|cleanup]")
        sys.exit(1)
        
    job_type = sys.argv[1].lower()
    
    if job_type == 'daily':
        run_daily_job()
    elif job_type == 'weekly':
        run_weekly_digest()
    elif job_type == 'cleanup':
        run_cleanup_job()
    else:
        print(f"Unknown job type: {job_type}")
        print("Valid options: daily, weekly, cleanup")
        sys.exit(1)
