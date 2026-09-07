#!/usr/bin/env bash
source venv/bin/activate
python -m uvicorn app.main:app --port 8002
