@echo off
echo ========================================
echo FIXR - Starting Application
echo ========================================
echo.

echo [1/4] Checking setup...
if not exist backend\.env (
    echo ERROR: backend\.env file not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

echo [2/4] Building frontend if needed...
if not exist frontend\dist (
    echo Building frontend...
    cd frontend
    call npm run build
    if %errorlevel% neq 0 (
        echo ERROR: Failed to build frontend
        pause
        exit /b 1
    )
    cd ..
) else (
    echo Frontend already built ✓
)

echo [3/4] Copying frontend to desktop...
cd desktop
call node copy-dist.js
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy frontend files
    pause
    exit /b 1
)
cd ..

echo [4/4] Starting application...
echo.
echo Starting Python backend server...
start "FIXR Backend" cmd /k "cd backend && python server.py"

echo Waiting for backend to start...
timeout /t 2 /nobreak >nul

echo Starting desktop application...
npm run electron

echo.
echo Application started!
echo - Backend server running in separate window
echo - Desktop app should show UI even if backend is offline
echo.
pause