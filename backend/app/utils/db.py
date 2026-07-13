

# import os
# from dotenv import load_dotenv

# # ASYNC driver (FastAPI)
# from motor.motor_asyncio import AsyncIOMotorClient

# # SYNC driver (collectors)
# from pymongo import MongoClient

# load_dotenv()

# MONGODB_URI = os.getenv("MONGODB_URI")
# DB_NAME = os.getenv("DB_NAME", "dataleak")

# # ---------- ASYNC (for FastAPI) ----------
# async_client = None
# async_db = None

# async def connect_db():
#     global async_client, async_db
#     async_client = AsyncIOMotorClient(MONGODB_URI)
#     async_db = async_client[DB_NAME]
#     print(">>> Async MongoDB connected")
#     return async_db

# async def close_db():
#     global async_client
#     if async_client:
#         async_client.close()
#         print(">>> Async MongoDB closed")

# # ---------- SYNC (for collectors) ----------
# sync_client = None
# db = None  # <-- collectors use this db

# def connect_sync():
#     global sync_client, db
#     sync_client = MongoClient(MONGODB_URI)  # <-- SYNC client
#     db = sync_client[DB_NAME]
#     print(">>> Sync MongoDB connected for collectors")
#     return db

import os
from dotenv import load_dotenv

# ASYNC driver (FastAPI)
from motor.motor_asyncio import AsyncIOMotorClient

# SYNC driver (collectors)
from pymongo import MongoClient

load_dotenv()

# -------------------------------
# Monitoring Project Database
# -------------------------------
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "dataleak")

# -------------------------------
# LMS Database
# -------------------------------
LMS_MONGODB_URI = os.getenv("LMS_MONGODB_URI")
LMS_DB_NAME = os.getenv("LMS_DB_NAME", "lms")

# =====================================================
# Monitoring Database (ASYNC)
# =====================================================

async_client = None
async_db = None


async def connect_db():
    global async_client, async_db

    async_client = AsyncIOMotorClient(MONGODB_URI)
    async_db = async_client[DB_NAME]

    print(">>> Monitoring MongoDB connected")

    return async_db


async def close_db():
    global async_client

    if async_client:
        async_client.close()
        print(">>> Monitoring MongoDB closed")


# =====================================================
# LMS Database (ASYNC)
# =====================================================

lms_async_client = None
lms_async_db = None


async def connect_lms_db():
    global lms_async_client, lms_async_db

    lms_async_client = AsyncIOMotorClient(LMS_MONGODB_URI)
    lms_async_db = lms_async_client[LMS_DB_NAME]

    print(">>> LMS MongoDB connected")

    return lms_async_db


async def close_lms_db():
    global lms_async_client

    if lms_async_client:
        lms_async_client.close()
        print(">>> LMS MongoDB closed")

 
# =====================================================
# Monitoring Database (SYNC)
# =====================================================

sync_client = None
db = None


def connect_sync():
    global sync_client, db

    sync_client = MongoClient(MONGODB_URI)
    db = sync_client[DB_NAME]

    print(">>> Sync Monitoring MongoDB connected")

    return db