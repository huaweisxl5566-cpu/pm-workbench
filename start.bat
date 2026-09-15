@echo off
echo ========================================
echo   PM Workbench - 项目经理工作台
echo ========================================
echo.
echo Starting both backend and frontend...
echo.

REM Start backend in new window
start "PM Workbench Backend" cmd /k "cd /d %~dp0 && start-backend.bat"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "PM Workbench Frontend" cmd /k "cd /d %~dp0 && start-frontend.bat"

echo.
echo ========================================
echo   Services are starting...
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
