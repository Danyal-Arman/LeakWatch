# # async MongoDB connection using motor
# from motor.motor_asyncio import AsyncIOMotorClient
# import os
# from dotenv import load_dotenv

# load_dotenv()  # reads .env

# MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
# DB_NAME = os.getenv("DB_NAME", "dataleak")

# client: AsyncIOMotorClient | None = None
# db = None

# async def connect_db():
#     global client, db
#     client = AsyncIOMotorClient(MONGODB_URI)
#     db = client[DB_NAME]
#     print(">>> MongoDB connected")
#     return db

# async def close_db():
#     global client
#     if client:
#         client.close() 


import os
from dotenv import load_dotenv

# ASYNC driver (FastAPI)
from motor.motor_asyncio import AsyncIOMotorClient

# SYNC driver (collectors)
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "dataleak")

# ---------- ASYNC (for FastAPI) ----------
async_client = None
async_db = None

async def connect_db():
    global async_client, async_db
    async_client = AsyncIOMotorClient(MONGODB_URI)
    async_db = async_client[DB_NAME]
    print(">>> Async MongoDB connected")
    return async_db

async def close_db():
    global async_client
    if async_client:
        async_client.close()
        print(">>> Async MongoDB closed")

# ---------- SYNC (for collectors) ----------
sync_client = None
db = None  # <-- collectors use this db

def connect_sync():
    global sync_client, db
    sync_client = MongoClient(MONGODB_URI)  # <-- SYNC client
    db = sync_client[DB_NAME]
    print(">>> Sync MongoDB connected for collectors")
    return db

