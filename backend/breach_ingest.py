import csv
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.processing.leak_rules import score_post

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "dataleak")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db.posts

CSV_FILE = "data/breaches.csv"


def build_text(row):
    """
    Build meaningful text from ANY Kaggle breach dataset
    """
    parts = []

    for key in row:
        value = row[key]
        if value and value.strip():
            parts.append(f"{key}: {value}")

    return " | ".join(parts)


def ingest_breaches(csv_file):
    inserted = 0

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        print("CSV Columns Detected:", reader.fieldnames)

        for i, row in enumerate(reader):
            text = build_text(row)

            # Skip empty rows
            if not text.strip():
                continue

            meta = score_post(text)

            doc = {
                "platform": "kaggle_breach",
                "post_id": f"breach_{i}",
                "text": text,
                "user": row.get("company") or row.get("Entity") or "unknown",
                "urls": [],
                "timestamp": None,
                "meta": meta
            }

            if not collection.find_one({"post_id": doc["post_id"]}):
                collection.insert_one(doc)
                inserted += 1

    print(f"Inserted {inserted} breach records into MongoDB")


if __name__ == "__main__":
    ingest_breaches(CSV_FILE)
