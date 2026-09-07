@echo off
call venv\Scripts\activate
python -m uvicorn app.main:app --port 8002
