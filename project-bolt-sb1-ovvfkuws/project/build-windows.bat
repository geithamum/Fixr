@echo off
echo ========================================
echo FIXR - Building Desktop Application
echo ========================================
echo.

echo [1/3] Building frontend...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)

echo.
echo [2/3] Copying files to desktop...
cd ..\desktop
call node copy-dist.js
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy files
    pause
    exit /b 1
)

echo.
echo [3/3] Building desktop executable...
call npx electron-builder --publish=never
if %errorlevel% neq 0 (
    echo ERROR: Desktop build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable created in: desktop\dist-electron\
echo.
pause