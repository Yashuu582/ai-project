from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: Optional[str] = "Applied"
    job_description: Optional[str] = None
    resume_text: Optional[str] = None
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    job_description: Optional[str] = None
    resume_text: Optional[str] = None
    notes: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str
    job_description: Optional[str]
    resume_text: Optional[str]
    ai_score: Optional[int]
    ai_feedback: Optional[str]
    notes: Optional[str]
    applied_date: datetime

    class Config:
        from_attributes = True

class AIAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
