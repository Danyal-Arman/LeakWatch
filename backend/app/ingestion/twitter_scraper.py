# import argparse
# import snscrape.modules.twitter as sntwitter
# from datetime import datetime
# from ..utils import db as db_module
# from ..processing.leak_rules import score_post


# def fetch_and_store(query="leak OR leaked OR dump OR credentials", limit=30):
#     # Connect to MongoDB (sync)
#     if db_module.db is None:
#         db_module.connect_sync()

#     collection = db_module.db.posts

#     scraped = 0
#     inserted = 0

#     print(f">>> Searching Twitter for: {query}")

#     for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
#         if scraped >= limit:
#             break

#         scraped += 1
#         text = tweet.content
#         meta = score_post(text)

#         doc = {
#             "platform": "twitter_scrape",
#             "post_id": str(tweet.id),
#             "text": text,
#             "user": str(tweet.user.username),
#             "urls": meta.get("urls", []),
#             "timestamp": int(tweet.date.timestamp()) if tweet.date else None,
#             "meta": meta,
#             "raw": {
#                 "username": tweet.user.username,
#                 "url": tweet.url,
#             },
#         }

#         # Prevent duplicates
#         if not collection.find_one({"post_id": str(tweet.id)}):
#             collection.insert_one(doc)
#             inserted += 1

#     return scraped, inserted


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--query", default="leak OR leaked OR dump OR credentials")
#     parser.add_argument("--limit", type=int, default=30)
#     args = parser.parse_args()

#     db_module.connect_sync()

#     try:
#         scraped, inserted = fetch_and_store(args.query, args.limit)
#         print(f">>> Scraped: {scraped}, Inserted: {inserted}")
#     except Exception as e:
#         print("Error:", e)
