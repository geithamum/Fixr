# FIXR - AI Problem Solver

A beautiful cross-platform desktop application for AI-powered problem solving.

## 🚀 Quick Start

### Windows
1. **Run `BUILD-EXE.bat`** - Creates portable executable
2. **Go to FIXR-READY folder**
3. **Double-click `RUN-FIXR.bat`**
4. **Add OpenAI API key** via Settings

### Development
1. **Run `setup-windows.bat`** - One-time setup
2. **Add OpenAI API key** to `backend\.env`
3. **Run `start-windows.bat`** - Launch app

## 📋 Prerequisites

- **Node.js** (v16+) - [Download here](https://nodejs.org)
- **Python** (v3.7+) - [Download here](https://python.org)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## 🏗️ Project Structure

```
├── frontend/          # React web application
├── desktop/           # Electron desktop wrapper
├── backend/           # Python backend server
├── BUILD-EXE.bat     # Create portable executable
├── setup-windows.bat # Development setup
└── start-windows.bat # Launch development app
```

## ✨ Features

- **Beautiful React UI** with gradient design
- **Real-time AI chat** with OpenAI GPT-3.5-turbo
- **Native desktop app** with custom window controls
- **Portable executable** - runs anywhere without installation
- **Python backend** auto-starts with the app

## 🔑 OpenAI API Setup

1. Get API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. For development: Add to `backend\.env`
3. For portable app: Add via Settings UI

## 🐛 Troubleshooting

### Node.js Issues
- Install from [nodejs.org](https://nodejs.org)
- Restart terminal after installation

### Build Issues
- Run as Administrator
- Temporarily disable antivirus
- Check internet connection

### Backend Issues
- Verify API key format (starts with `sk-`)
- Check OpenAI account has credits
- Ensure port 8080 is available

## 👥 Credits

- **Neil Bhalla** - Frontend & Integration
- **Geith Amum** - Backend & Architecture
