from fastapi import FastAPI
from .routes import posts
from .utils.db import connect_db, close_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DataLeak Sentinel - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db():
    print(">>> CONNECT_DB CALLED")
    await connect_db()

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()

app.include_router(posts.router)  

@app.get("/health")
async def health():
    return {"status": "ok"}
