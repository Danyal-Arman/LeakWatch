from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    platform: str
    post_id: str
    text: str
    user: Optional[str] = None
    urls: Optional[List[str]] = []
    timestamp: Optional[datetime] = None

class PostInDB(PostCreate):
    id: str = Field(None, alias="_id")
