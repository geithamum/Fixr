# FIXR - Windows Quick Start Guide

## 🚀 Super Simple Setup (3 steps)

### 1. Run Setup
Double-click: **`setup-windows.bat`**

This will:
- Install all dependencies
- Build the frontend
- Create the backend configuration file

### 2. Get OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-`)
4. Edit `backend\.env` file and replace `your_openai_api_key_here` with your actual key

### 3. Start the App
Double-click: **`start-windows.bat`**

That's it! The app will start automatically.

## 📁 Batch Files Included

| File | Purpose |
|------|---------|
| `setup-windows.bat` | One-time setup (install dependencies, build) |
| `start-windows.bat` | Start the application (production mode) |
| `start-dev-windows.bat` | Start in development mode (with hot reload) |
| `build-windows.bat` | Build standalone executable |

## 🔧 Manual Commands (if needed)

If the batch files don't work, you can run these commands in PowerShell:

```powershell
# Setup
cd frontend && npm install && cd ../desktop && npm install && cd ../frontend && npm run build && cd ..

# Start backend (in separate terminal)
cd backend && python server.py

# Start desktop app (in another terminal)
cd desktop && npm run electron
```

## 🐛 Troubleshooting

### "Python not found"
- Install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### "npm not found"
- Install Node.js from [nodejs.org](https://nodejs.org)
- Restart your terminal after installation

### "OpenAI API Error"
- Check your API key in `backend\.env`
- Make sure you have credits in your OpenAI account
- Verify the key starts with `sk-`

### Backend won't start
- Make sure port 8080 is not in use
- Check Windows Firewall settings
- Try running as administrator

## 📦 Building Executable

To create a standalone `.exe` file:
1. Run `build-windows.bat`
2. Find the executable in `desktop\dist-electron\`
3. You can distribute this file to other Windows computers

## 🎯 What Each Component Does

- **Frontend**: React web interface (runs in Electron)
- **Desktop**: Electron wrapper (makes it a native Windows app)
- **Backend**: Python server (handles OpenAI API calls)

The desktop app automatically connects to the Python backend running on your computer.