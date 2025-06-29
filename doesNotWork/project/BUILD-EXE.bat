@echo off
title FIXR - Build Portable Executable
echo.
echo ========================================
echo    FIXR - Portable EXE Builder
echo ========================================
echo.
echo This will create a portable .exe that runs instantly!
echo Time needed: 2-5 minutes
echo.
pause

echo [1/8] Cleaning previous builds...
if exist desktop\dist rmdir /s /q desktop\dist
if exist desktop\dist-electron rmdir /s /q desktop\dist-electron
if exist FIXR-READY rmdir /s /q FIXR-READY

echo [2/8] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo [3/8] Installing desktop dependencies (including Electron)...
cd ..\desktop
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install desktop dependencies
    pause
    exit /b 1
)

echo [4/8] Building frontend...
cd ..\frontend
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)

echo [5/8] Preparing desktop app...
cd ..\desktop
call node copy-dist.js
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy frontend files
    pause
    exit /b 1
)

echo [6/8] Copying backend files...
if exist backend rmdir /s /q backend
mkdir backend
xcopy /s /e /i ..\backend backend
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy backend files
    pause
    exit /b 1
)

echo [7/8] Creating portable executable...
echo Building with electron-builder...
call npx electron-builder --win portable --publish=never
if %errorlevel% neq 0 (
    echo ERROR: Executable build failed
    echo.
    echo Troubleshooting:
    echo - Make sure you have internet connection
    echo - Try running as Administrator
    echo - Check if antivirus is blocking the build
    pause
    exit /b 1
)

echo [8/8] Setting up ready folder...
cd ..
mkdir FIXR-READY 2>nul

echo Looking for built executable...
for %%f in (desktop\dist-electron\FIXR-Portable-*.exe) do (
    echo Found: %%f
    copy "%%f" "FIXR-READY\"
    set "EXE_NAME=%%~nxf"
)

if not exist "FIXR-READY\FIXR-Portable-*.exe" (
    echo ERROR: Executable not found in desktop\dist-electron\
    echo Checking what was built...
    dir desktop\dist-electron\
    pause
    exit /b 1
)

cd FIXR-READY
echo @echo off > RUN-FIXR.bat
echo echo Starting FIXR... >> RUN-FIXR.bat
echo start "" "FIXR-Portable-1.0.0.exe" >> RUN-FIXR.bat

echo.
echo ========================================
echo SUCCESS! Portable executable ready!
echo ========================================
echo.
echo Location: FIXR-READY\
echo.
echo Files created:
dir /b
echo.
echo To run: Double-click RUN-FIXR.bat
echo.
echo IMPORTANT: The backend Python server is now embedded!
echo Your OpenAI API key will be saved in the app's data folder.
echo.
pause