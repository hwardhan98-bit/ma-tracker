import feedparser
import os
from dateutil import parser as date_parser
from supabase import create_client, Client

# This securely grabs your Supabase keys from GitHub later
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# The list of companies you want to track. Edit this as you like!
TRACK_LIST = [
    {"name": "Apple", "industry": "Technology"},
    {"name": "Microsoft", "industry": "Technology"},
    {"name": "Exxon", "industry": "Energy"}
]

def fetch_news():
    deals = []
    for target in TRACK_LIST:
        company = target["name"]
        industry = target["industry"]
        
        # We use Google News RSS to search for the company AND (merger OR acquisition)
        url = f'https://news.google.com/rss/search?q="{company}"+AND+(merger+OR+acquisition)&hl=en-US&gl=US&ceid=US:en'
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            # Clean up the title to find the original source name
            title_parts = entry.title.split(" - ")
            source = title_parts[-1] if len(title_parts) > 1 else "Unknown"
            
            deals.append({
                "title": entry.title,
                "url": entry.link,
                "company": company,
                "industry": industry,
                "published_at": date_parser.parse(entry.published).isoformat(),
                "source": source
            })
    return deals

def save_to_supabase(deals):
    if not deals: return
    
    for deal in deals:
        try:
             # Upsert prevents duplicate news articles from being saved twice
             supabase.table("ma_deals").upsert(deal, on_conflict="url").execute()
        except Exception:
            pass 

if __name__ == "__main__":
    deals = fetch_news()
    save_to_supabase(deals)