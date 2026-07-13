from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class RuleMeta(BaseModel):
    score: int
    severity: str
    flags: List[str]


class AIResult(BaseModel):
    isLeak: bool
    severity: str
    confidence: int
    reason: str


class SecurityReportCreate(BaseModel):
    name: str
    email: EmailStr

    meta: RuleMeta

    ai: Optional[AIResult] = None

    emailSent: bool = False

    status: str = "open"          # open / resolved

    createdAt: datetime = datetime.utcnow()

    updatedAt: Optional[datetime] = None



class SecurityReportInDB(SecurityReportCreate):
    id: str | None = None