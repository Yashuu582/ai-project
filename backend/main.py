from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, ai_service
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS with AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/applications", response_model=List[schemas.ApplicationOut])
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.Application).order_by(models.Application.applied_date.desc()).all()

@app.post("/applications", response_model=schemas.ApplicationOut)
def create_application(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    app_obj = models.Application(**data.model_dump())
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@app.put("/applications/{app_id}", response_model=schemas.ApplicationOut)
def update_application(app_id: int, data: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(app_obj, key, value)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@app.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app_obj)
    db.commit()
    return {"message": "Deleted"}

@app.post("/applications/{app_id}/analyze")
def analyze_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    if not app_obj.resume_text or not app_obj.job_description:
        raise HTTPException(status_code=400, detail="Both resume and job description are required for AI analysis")

    result = ai_service.analyze_resume(app_obj.resume_text, app_obj.job_description)

    app_obj.ai_score = result.get("score", 0)
    app_obj.ai_feedback = str(result)
    db.commit()
    db.refresh(app_obj)
    return result

@app.post("/analyze", response_model=dict)
def quick_analyze(data: schemas.AIAnalyzeRequest):
    return ai_service.analyze_resume(data.resume_text, data.job_description)

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    apps = db.query(models.Application).all()
    statuses = {}
    for a in apps:
        statuses[a.status] = statuses.get(a.status, 0) + 1
    return {"total": len(apps), "by_status": statuses}
