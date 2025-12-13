import os
import argparse
from dotenv import load_dotenv
import tweepy
from ..utils import db as db_module
from ..processing.leak_rules import score_post

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)


def fetch_and_store(query: str = "leak OR leaked OR dump OR credentials", max_results: int = 50):
    if db_module.db is None:
        raise RuntimeError("Database is not connected. Start the FastAPI app so startup connects DB.")

    collection = db_module.db.posts

    # tweepy.Client.search_recent_tweets returns Response with data list
    resp = client.search_recent_tweets(query=query, max_results=min(max_results, 100), tweet_fields=["created_at","author_id","entities"], expansions=None)
    tweets = resp.data or []
    inserted = 0
    for t in tweets:
        text = t.text
        meta = score_post(text)
        doc = {
            "platform": "twitter",
            "post_id": str(t.id),
            "text": text,
            "user": str(t.author_id) if hasattr(t, "author_id") else None,
            "urls": meta.get("urls", []),
            "timestamp": int(t.created_at.timestamp()) if t.created_at else None,
            "meta": meta,
            "raw": t.data if hasattr(t, "data") else {},
        }
        existing = collection.find_one({"post_id": str(t.id)})
        if not existing:
            collection.insert_one(doc)
            inserted += 1
    return inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="leak OR leaked OR dump OR credentials")
    parser.add_argument("--max", type=int, default=50)
    args = parser.parse_args()

    try:
        n = fetch_and_store(args.query, args.max)
        print(f"Inserted {n} tweets")
    except Exception as e:
        print("Error:", e)