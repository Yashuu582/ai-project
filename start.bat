@echo off
echo Starting ATS Backend...
cd backend
python -m uvicorn main:app --reload --port 8000
