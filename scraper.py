import feedparser
import os
import re
import urllib.parse
from dateutil import parser as date_parser
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# The 13 Sectors
INDUSTRIES = [
    "Technology", "Healthcare", "Energy", "Finance", "Real Estate", 
    "Consumer Goods", "Retail", "Manufacturing", "Telecommunications", 
    "Media", "Transportation", "Agriculture", "Utilities"
]

def extract_deal_info(title):
    title_lower = title.lower()
    
    # 1. Guess Deal Type
    deal_type = "Acquisition" # Default
    if "merger" in title_lower: deal_type = "Merger"
    elif "take-private" in title_lower or "private equity" in title_lower: deal_type = "Take-Private"
    elif "carve-out" in title_lower or "spinoff" in title_lower: deal_type = "Carve-out"
    elif "joint venture" in title_lower or " jv " in title_lower: deal_type = "Joint Venture"

    # 2. Guess Region
    region = "Global/Unknown"
    if any(w in title_lower for w in [" us ", " u.s.", "american"]): region = "North America"
    elif any(w in title_lower for w in ["uk ", "europe", "eu "]): region = "Europe"
    elif any(w in title_lower for w in ["china", "japan", "india", "asia"]): region = "Asia-Pacific"

    # 3. Extract Deal Value
    deal_value = None
    value_match = re.search(r'\$\s*([0-9,.]+)\s*(billion|million|b|m)', title_lower, re.IGNORECASE)
    if value_match:
        number = float(value_match.group(1).replace(',', ''))
        magnitude = value_match.group(2).lower()
        if magnitude.startswith('b'):
            deal_value = number * 1000 # Convert to millions
        elif magnitude.startswith('m'):
            deal_value = number
            
    return deal_type, region, deal_value

def fetch_news():
    deals = []
    for industry in INDUSTRIES:
        # Safely format and encode the URL to fix space/character errors
        raw_query = f'"{industry}" AND (merger OR acquisition OR "joint venture") when:1d'
        encoded_query = urllib.parse.quote(raw_query)
        url = f'https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en'
        
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            title_parts = entry.title.split(" - ")
            source = title_parts[-1] if len(title_parts) > 1 else "Unknown"
            clean_title = " - ".join(title_parts[:-1]) if len(title_parts) > 1 else entry.title
            
            deal_type, region, deal_value = extract_deal_info(clean_title)
            
            deals.append({
                "title": clean_title,
                "url": entry.link,
                "company": "Various",
                "industry": industry,
                "source": source,
                "published_at": date_parser.parse(entry.published).isoformat(),
                "deal_type": deal_type,
                "region": region,
                "deal_value": deal_value
            })
    return deals

def save_to_supabase(deals):
    if not deals: return
    for deal in deals:
        try:
             supabase.table("ma_deals").upsert(deal, on_conflict="url").execute()
        except Exception:
            pass 

if __name__ == "__main__":
    deals = fetch_news()
    save_to_supabase(deals)
