import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

from database import init_db, is_duplicate, mark_as_posted, cleanup_old_entries, get_weekly_stats
from collector import fetch_rss_feeds
from processor import extract_summary, format_post
from formatter import format_weekly_digest
from telegram_bot import send_telegram_message_sync
from config import TIMEZONE, MAX_POSTS_PER_DAY

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

# Global tracker for rate limiting
daily_posts_count = 0

def reset_daily_counter():
    global daily_posts_count
    daily_posts_count = 0
    logging.info("Daily post counter reset.")

def run_daily_job():
    global daily_posts_count
    logging.info("Starting daily job to fetch and post numismatic news.")
    
    if daily_posts_count >= MAX_POSTS_PER_DAY:
        logging.info("Max daily posts reached. Skipping job.")
        return

    init_db()
    
    articles = fetch_rss_feeds()
    if not articles:
        logging.info("No relevant articles found.")
        return

    posted_this_run = 0
    for article in articles:
        if daily_posts_count >= MAX_POSTS_PER_DAY:
            break
            
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
            daily_posts_count += 1
            posted_this_run += 1
            logging.info(f"Successfully posted article. Daily count: {daily_posts_count}")
                
        # Limit to 3 posts per job run as requested in "Daily top 3 numismatic news posts"
        if posted_this_run >= 3:
            break

def run_weekly_digest():
    logging.info("Starting weekly digest job.")
    init_db()
    count, sources = get_weekly_stats()
    
    # We can fetch recent articles from db or feed. The requirement asks for "Top 10 Coins digest post".
    # For simplicity, we fetch from feeds again and format the top ones.
    articles = fetch_rss_feeds()
    
    digest_text = format_weekly_digest(articles, count, sources)
    send_telegram_message_sync(digest_text)
    logging.info("Weekly digest posted.")

def run_cleanup_job():
    init_db()
    cleanup_old_entries(days=30)

if __name__ == "__main__":
    logging.info("Starting Numismatics Bot Scheduler...")
    init_db()
    
    scheduler = BlockingScheduler(timezone=timezone(TIMEZONE))
    
    # Reset counter at midnight
    scheduler.add_job(reset_daily_counter, 'cron', hour=0, minute=0)
    
    # 9:00 AM: Daily top 3 numismatic news posts
    scheduler.add_job(run_daily_job, 'cron', hour=9, minute=0)
    
    # 6:00 PM: Heritage/archaeology update post
    scheduler.add_job(run_daily_job, 'cron', hour=18, minute=0)
    
    # Every Sunday 10:00 AM: Weekly digest
    scheduler.add_job(run_weekly_digest, 'cron', day_of_week='sun', hour=10, minute=0)
    
    # Weekly cleanup job (Sunday at midnight)
    scheduler.add_job(run_cleanup_job, 'cron', day_of_week='sun', hour=0, minute=5)
    
    logging.info("Scheduler initialized. Waiting for jobs...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
