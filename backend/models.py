from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    status = Column(String(50), default="Applied")  # Applied, Interview, Offer, Rejected
    job_description = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True)
    ai_score = Column(Integer, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    applied_date = Column(DateTime, default=datetime.utcnow)
