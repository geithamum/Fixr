@echo off
echo ========================================
echo FIXR - Development Mode
echo ========================================
echo.

echo Starting Python backend server...
start "FIXR Backend" cmd /k "cd backend && python server.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting development server...
npm run dev-desktop

pause