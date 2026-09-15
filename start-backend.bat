@echo off
echo ========================================
echo   PM Workbench - Starting Backend...
echo ========================================

cd /d "%~dp0backend"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and install deps
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting FastAPI server on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000
