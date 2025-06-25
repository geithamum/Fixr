#!/bin/bash

echo "========================================"
echo "FIXR - Starting Application"
echo "========================================"
echo

echo "Checking if backend/.env exists..."
if [ ! -f backend/.env ]; then
    echo "ERROR: backend/.env file not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

echo "Starting Python backend server..."
cd backend
python3 server.py &
BACKEND_PID=$!
cd ..

echo "Backend started with PID: $BACKEND_PID"
echo "Waiting for backend to initialize..."
sleep 3

echo "Starting desktop application..."
cd desktop
npm run electron

echo
echo "Cleaning up..."
kill $BACKEND_PID 2>/dev/null
echo "Application stopped."