#!/bin/bash

echo "========================================"
echo "FIXR - Linux/macOS Setup Script"
echo "========================================"
echo

echo "[1/4] Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    exit 1
fi

echo
echo "[2/4] Installing desktop dependencies..."
cd ../desktop
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install desktop dependencies"
    exit 1
fi

echo
echo "[3/4] Building frontend..."
cd ../frontend
npm run build
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build frontend"
    exit 1
fi

echo
echo "[4/4] Setting up backend environment..."
cd ../backend
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo
    echo "IMPORTANT: Edit backend/.env and add your OpenAI API key!"
    echo "Get your API key from: https://platform.openai.com/api-keys"
    echo
fi

cd ..
echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Edit backend/.env and add your OpenAI API key"
echo "2. Run ./start.sh to launch the application"
echo