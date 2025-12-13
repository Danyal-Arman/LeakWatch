# backend/app/routes/posts.py
from fastapi import APIRouter, HTTPException
from typing import List
from ..utils import db as db_module
from ..models.post_model import PostCreate

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[dict])
async def list_posts(limit: int = 20):
    database = db_module.db
    if database is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    cursor = database.posts.find().sort("timestamp", -1).limit(limit)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results

@router.post("/", status_code=201)
async def create_post(payload: PostCreate):
    database = db_module.db
    if database is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    doc = payload.dict()
    res = await database.posts.insert_one(doc)
    created = await database.posts.find_one({"_id": res.inserted_id})
    created["_id"] = str(created["_id"])
    return created
