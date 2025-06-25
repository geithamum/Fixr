#!/bin/bash

echo "========================================"
echo "FIXR - Development Mode"
echo "========================================"
echo

echo "Starting Python backend server..."
cd backend
python3 server.py &
BACKEND_PID=$!
cd ..

echo "Backend started with PID: $BACKEND_PID"
echo "Waiting for backend to initialize..."
sleep 3

echo "Starting development server..."
cd desktop
npm run dev-desktop

echo
echo "Cleaning up..."
kill $BACKEND_PID 2>/dev/null
echo "Development server stopped."