# sample_leak_generator.py
# Project: Social Media Monitoring for Data Leaks
# Purpose: Generate demo/sample leak data for testing & presentation

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "dataleak")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db.posts


LEAK_TEXTS = [
    "Database leak detected: 50,000 user emails exposed example1@gmail.com",
    "Credential dump found containing admin@test.com and passwords",
    "Leaked customer data posted online, contact: support@company.com",
    "Massive data breach reported, emails like user123@yahoo.com leaked",
    "Hackers claim leaked database with employee emails hr@org.com",
]

USERS = ["threat_actor_1", "cyber_watch", "anon_leaker", "datahunter", "security_news"]

URLS = [
    "https://pastebin.com/example",
    "https://mega.nz/file/example",
    "https://anonfiles.com/example",
]


def generate_post(i):
    text = random.choice(LEAK_TEXTS)
    return {
        "platform": "demo",
        "post_id": f"demo_{int(time.time())}_{i}",
        "text": text,
        "user": random.choice(USERS),
        "urls": [random.choice(URLS)],
        "timestamp": int(time.time()),
        "meta": {
            "severity": "high",
            "source": "demo_generator"
        }
    }


def main(count=10):
    inserted = 0
    for i in range(count):
        doc = generate_post(i)
        collection.insert_one(doc)
        inserted += 1
    print(f"Inserted {inserted} sample leak records for demo")


if __name__ == "__main__":
    main(10)
