#!/bin/bash

echo "========================================"
echo "FIXR - Building Desktop Application"
echo "========================================"
echo

echo "[1/3] Building frontend..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed"
    exit 1
fi

echo
echo "[2/3] Copying files to desktop..."
cd ../desktop
node copy-dist.js
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to copy files"
    exit 1
fi

echo
echo "[3/3] Building desktop executable..."
npx electron-builder --publish=never
if [ $? -ne 0 ]; then
    echo "ERROR: Desktop build failed"
    exit 1
fi

echo
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo
echo "Executable created in: desktop/dist-electron/"
echo