from fastapi import APIRouter, HTTPException, Query
from ..utils import db as db_module
from ..models.post_model import PostCreate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
async def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    database = db_module.async_db
    if database is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    skip = (page - 1) * limit

    cursor = (
        database.posts
        .find()
        .sort("timestamp", -1)
        .skip(skip)
        .limit(limit)
    )

    posts = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        posts.append(doc)

    total = await database.posts.count_documents({})

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
        "data": posts
    }


@router.post("/", status_code=201)
async def create_post(payload: PostCreate):
    database = db_module.async_db
    if database is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    doc = payload.dict()
    res = await database.posts.insert_one(doc)
    created = await database.posts.find_one({"_id": res.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@router.delete("/all")
async def delete_all_posts():
    database = db_module.async_db
    if database is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    result = await database.posts.delete_many({})
    return {"deleted_count": result.deleted_count}
