@echo off
echo ========================================
echo FIXR - Windows Setup Script
echo ========================================
echo.

echo [1/4] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing desktop dependencies...
cd ..\desktop
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install desktop dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Building frontend...
cd ..\frontend
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend
    pause
    exit /b 1
)

echo.
echo [4/4] Setting up backend environment...
cd ..\backend
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo.
    echo IMPORTANT: Edit backend\.env and add your OpenAI API key!
    echo Get your API key from: https://platform.openai.com/api-keys
    echo.
)

cd ..
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your OpenAI API key
echo 2. Run start-windows.bat to launch the application
echo.
pause