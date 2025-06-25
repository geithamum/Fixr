# 🚀 FIXR Setup Instructions - PowerShell Fix

## ⚡ **Quick Fix for PowerShell**

You're using PowerShell, which requires `.\` before batch files. Use these commands:

```powershell
# Step 1: Run setup (one time only)
.\setup-windows.bat

# Step 2: Add your OpenAI API key to backend\.env

# Step 3: Start the application
.\start-windows.bat
```

## 📋 **Complete Setup Process**

### **Step 1: Run Setup**
```powershell
PS C:\Users\Neil_\Downloads\project-bolt-sb1-ovvfkuws\project> .\setup-windows.bat
```

This will:
- ✅ Install frontend dependencies
- ✅ Install desktop dependencies  
- ✅ Build the frontend
- ✅ Create backend/.env file

### **Step 2: Add OpenAI API Key**
1. Open the file: `backend\.env`
2. Replace: `OPENAI_API_KEY=your_openai_api_key_here`
3. With: `OPENAI_API_KEY=sk-your-actual-key-here`

Get your API key from: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### **Step 3: Start the Application**
```powershell
PS C:\Users\Neil_\Downloads\project-bolt-sb1-ovvfkuws\project> .\start-windows.bat
```

This will:
- ✅ Start Python backend server (in separate window)
- ✅ Copy frontend files to desktop
- ✅ Launch the desktop application

## 🎯 **Alternative: Use Command Prompt**

If you prefer Command Prompt over PowerShell:

```cmd
# Open Command Prompt (cmd)
# Navigate to your project folder
cd C:\Users\Neil_\Downloads\project-bolt-sb1-ovvfkuws\project

# Run setup (no .\ needed in cmd)
setup-windows.bat

# Start app (no .\ needed in cmd)  
start-windows.bat
```

## 🔍 **What Each Step Does**

### **Setup Process:**
1. **Frontend Dependencies**: Installs React, Vite, Tailwind CSS
2. **Desktop Dependencies**: Installs Electron, build tools
3. **Frontend Build**: Creates optimized production files
4. **Backend Config**: Creates .env file for your API key

### **Start Process:**
1. **Backend Check**: Verifies .env file exists
2. **Frontend Copy**: Copies built files to desktop app
3. **Python Server**: Starts backend on port 8080
4. **Desktop App**: Launches Electron window

## ✅ **Success Indicators**

### **Setup Success:**
- No red error messages
- "Setup Complete!" message appears
- `backend\.env` file is created
- `frontend\dist` folder exists

### **Start Success:**
- Backend terminal window opens
- Desktop app window opens with beautiful purple UI
- Status shows "Connected to OpenAI" (if API key is correct)
- You can type messages and get AI responses

## 🐛 **Common Issues & Fixes**

### **"Python not found"**
```powershell
# Check if Python is installed
python --version

# If not found, install from python.org
# Make sure to check "Add Python to PATH"
```

### **"npm not found"**
```powershell
# Check if Node.js is installed
node --version
npm --version

# If not found, install from nodejs.org
```

### **"Backend offline" in app**
- Check if Python backend window opened
- Look for errors in the backend terminal
- Verify your OpenAI API key in `backend\.env`
- Make sure port 8080 isn't blocked

### **Desktop app shows error page**
- This means frontend wasn't built properly
- Re-run: `.\setup-windows.bat`
- Check for errors during the build process

## 🎮 **Daily Usage (After Setup)**

Once everything is set up, you only need:

```powershell
.\start-windows.bat
```

This starts everything automatically!

## 📁 **File Structure Check**

After setup, you should have:
```
project/
├── .\setup-windows.bat     ← Run this first
├── .\start-windows.bat     ← Run this to start
├── frontend/
│   ├── dist/              ← Built files (created by setup)
│   └── node_modules/      ← Dependencies (created by setup)
├── desktop/
│   ├── dist/              ← Copied frontend files
│   └── node_modules/      ← Dependencies (created by setup)
└── backend/
    ├── .env               ← Your API key goes here
    ├── server.py          ← Python backend
    └── message.py         ← OpenAI integration
```

## 🆘 **Still Having Issues?**

### **Manual Commands (if scripts fail):**
```powershell
# Install dependencies
cd frontend
npm install
cd ..\desktop  
npm install

# Build frontend
cd ..\frontend
npm run build

# Copy files
cd ..\desktop
node copy-dist.js

# Start backend (separate terminal)
cd ..\backend
python server.py

# Start desktop (another terminal)
cd ..\
npm run electron
```

### **Reset Everything:**
```powershell
# Delete build folders
Remove-Item -Recurse -Force frontend\node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force desktop\node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force frontend\dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force desktop\dist -ErrorAction SilentlyContinue

# Run setup again
.\setup-windows.bat
```

The key difference is using `.\` before batch files in PowerShell! 🚀