from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime

from app.processing.password_rules import analyze_password
from app.services.ai_detector import ai_detect
from app.services.email_service import send_security_email
from app.utils import db as db_module

router = APIRouter(prefix="/security", tags=["Security"])


class PasswordRequest(BaseModel):
    name: str
    email: str
    password: str


@router.post("/analyze-password")
async def analyze_password_api(data: PasswordRequest):

    database = db_module.async_db

    if database is None:
        return {
            "success": False,
            "message": "Database not connected"
        }

    # Rule-based Detection
    result = analyze_password(data.password)

    ai_result = None

    status = "resolved"
    # AI Detection
    if result["score"] >= 70:
        ai_result = ai_detect(data.password)
        status = "open"

    # Save Report
    await database.security_reports.update_one(
        {"email": data.email},
        {
            "$set": {
                "name": data.name,
                "email": data.email,
                "meta": result,
                "ai": ai_result,
                "status": status,
                "emailSent": False,
                "createdAt": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    # Send Email
    if (
        ai_result is not None
        and result["score"] >= 70
        and ai_result["isWeak"]
    ):

        send_security_email(
            data.name,
            data.email,
            {
                **result,
                "ai": ai_result,
            },
        )

        await database.security_reports.update_one(
            {"email": data.email},
            {
                "$set": {
                    "emailSent": True
                }
            }
        )

    print("===================================")
    print("Name:", data.name)
    print("Email:", data.email)
    print("Result:", result)
    print("AI:", ai_result)
    print("===================================")

    return {
        "success": True,
        "report": {
            **result,
            "ai": ai_result
        }
    }


# ==========================================
# GET ALL SECURITY REPORTS
# ==========================================

@router.get("/reports")
async def get_security_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):

    database = db_module.async_db

    if database is None:
        return {
            "success": False,
            "message": "Database not connected"
        }

    skip = (page - 1) * limit

    cursor = (
        database.security_reports
        .find()
        .sort("createdAt", -1)
        .skip(skip)
        .limit(limit)
    )

    reports = []

    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        reports.append(doc)

    total = await database.security_reports.count_documents({})

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
        "data": reports,
    }