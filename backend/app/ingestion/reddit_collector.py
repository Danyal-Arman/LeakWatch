
import os
import time
import argparse
from dotenv import load_dotenv
import praw
from ..utils import db as db_module
from ..processing.leak_rules import score_post

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "DataLeakSentinel/0.1")

reddit = praw.Reddit( 
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)


def fetch_and_store(query: str = "leak|leaked|dump|credentials", limit: int = 50, subreddit: str = None):
    """Fetch submissions and insert into MongoDB with leak scoring."""
    if db_module.db is None:
        raise RuntimeError("Database is not connected. Start the FastAPI app so startup connects DB.")

    collection = db_module.db.posts

    if subreddit:
        submissions = reddit.subreddit(subreddit).search(query, sort="new", limit=limit)
    else:
        submissions = reddit.subreddit("all").search(query, sort="new", limit=limit)

    inserted = 0
    for sub in submissions:
        text = (sub.title or "") + "\n" + (sub.selftext or "")
        meta = score_post(text)
        doc = {
            "platform": "reddit",
            "post_id": sub.id,
            "text": text,
            "user": str(sub.author) if sub.author else None,
            "urls": [u for u in sub.url and [sub.url] or []],
            "timestamp": int(sub.created_utc),
            "meta": meta,
            "raw": {
                "title": sub.title,
                "selftext": sub.selftext,
                "permalink": sub.permalink,
            },
        }
        existing = collection.find_one({"post_id": sub.id})
        if not existing:
            collection.insert_one(doc)
            inserted += 1
    return inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="leak|leaked|dump|credentials")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--subreddit", default=None)
    args = parser.parse_args()

    #
    try:
        n = fetch_and_store(args.query, args.limit, args.subreddit)
        print(f"Inserted {n} reddit posts")
    except Exception as e:
        print("Error:", e)