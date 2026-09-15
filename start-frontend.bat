@echo off
echo ========================================
echo   PM Workbench - Starting Frontend...
echo ========================================

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo.
echo Starting Vue dev server on http://localhost:3000
echo Press Ctrl+C to stop
echo.
npm run dev
