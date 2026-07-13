import asyncio

from app.utils.db import connect_db, close_db
from app.processing.leak_rules import score_post
from app.services.ai_detector import ai_detect

async def process_ai():
    database = await connect_db()
    try:
        posts = await database.posts.find().to_list()

        for post in posts:
            text = post.get("text", "")
            result = score_post(text)

            if result["score"] >= 70:
                ai_result = ai_detect(text)

                await database.posts.update_one(
                    {"_id": post["_id"]},
                    {
                        "$set": {
                            "meta": result,
                            "ai": ai_result
                        }
                    }
                )
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(process_ai())