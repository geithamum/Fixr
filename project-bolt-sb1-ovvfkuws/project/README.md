# FIXR - AI Problem Solver

A beautiful cross-platform desktop and web application for AI-powered problem solving with Python backend integration.

## 🚀 Quick Start

### Windows
1. **Double-click `setup-windows.bat`** - Installs everything
2. **Add OpenAI API key** to `backend\.env`
3. **Double-click `start-windows.bat`** - Launches the app

### Linux/macOS
1. **Run `./setup.sh`** - Installs everything
2. **Add OpenAI API key** to `backend/.env`
3. **Run `./start.sh`** - Launches the app

## 📋 Prerequisites

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org)
- **Python** (v3.7 or higher) - [Download here](https://python.org)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## 🎯 Platform-Specific Scripts

### Windows (.bat files)
| File | Purpose |
|------|---------|
| `setup-windows.bat` | One-time setup |
| `start-windows.bat` | Start application |
| `start-dev-windows.bat` | Development mode |
| `build-windows.bat` | Build executable |

### Linux/macOS (.sh files)
| File | Purpose |
|------|---------|
| `setup.sh` | One-time setup |
| `start.sh` | Start application |
| `start-dev.sh` | Development mode |
| `build.sh` | Build executable |

## 🔧 Manual Setup (if scripts fail)

### 1. Install Dependencies
```bash
# Frontend
cd frontend && npm install

# Desktop
cd ../desktop && npm install

# Build frontend
cd ../frontend && npm run build
```

### 2. Configure Backend
```bash
cd backend
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Start Application
```bash
# Terminal 1: Start backend
cd backend
python server.py    # Windows
python3 server.py   # Linux/macOS

# Terminal 2: Start desktop app
cd desktop
npm run electron
```

## 🏗️ Project Structure

```
├── frontend/          # React web application
├── desktop/           # Electron desktop wrapper
├── backend/           # Python backend server
├── setup-windows.bat  # Windows setup script
├── start-windows.bat  # Windows start script
├── setup.sh          # Linux/macOS setup script
├── start.sh          # Linux/macOS start script
└── README.md         # This file
```

## ✨ Features

### 🎨 Frontend (React + Vite)
- Beautiful gradient UI with custom scrollbars
- Real-time chat interface with OpenAI integration
- Quick action buttons for common tasks
- Responsive design with Tailwind CSS
- TypeScript support

### 🖥️ Desktop (Electron)
- Native desktop experience on Windows, Linux, macOS
- Custom window controls (minimize, maximize, close)
- Frameless window design
- Cross-platform compatibility
- Auto-detects and connects to Python backend

### 🤖 Backend (Python + OpenAI)
- OpenAI GPT-3.5-turbo integration
- Simple HTTP server with CORS support
- Environment-based configuration
- Error handling and timeout management
- Health check endpoint

## 🔑 OpenAI API Setup

1. **Get API Key**: Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. **Create Key**: Click "Create new secret key"
3. **Copy Key**: Save the key (starts with `sk-`)
4. **Add to .env**: Edit `backend/.env` or `backend\.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

## 🎮 Window Controls

The desktop version includes custom window controls in the top-right corner:
- **Yellow button**: Minimize window
- **Green button**: Maximize/restore window  
- **Red button**: Close application

## 📊 Backend Status Indicator

The UI shows real-time backend connection status:
- **🟢 Green**: Backend online and responding
- **🔴 Red**: Backend offline or unreachable
- **🟡 Yellow**: Checking connection status

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev
```

### Desktop Development
```bash
# Linux/macOS
./start-dev.sh

# Windows
start-dev-windows.bat
```

### Backend Development
```bash
cd backend
python server.py    # Windows
python3 server.py   # Linux/macOS
```

## 📦 Building Executables

### Windows
```bash
build-windows.bat
```

### Linux/macOS
```bash
./build.sh
```

Executables will be created in `desktop/dist-electron/`

## 🐛 Troubleshooting

### Python Issues
- **Windows**: Install from [python.org](https://python.org), check "Add to PATH"
- **Linux**: `sudo apt install python3` or `sudo yum install python3`
- **macOS**: `brew install python3` or install from [python.org](https://python.org)

### Node.js Issues
- Install from [nodejs.org](https://nodejs.org)
- Restart terminal after installation
- Verify with: `node --version` and `npm --version`

### OpenAI API Issues
- Check API key format (starts with `sk-`)
- Verify account has credits/billing set up
- Check rate limits in OpenAI dashboard
- Ensure `.env` file is in `backend/` directory

### Port 8080 In Use
```bash
# Find process using port 8080
netstat -ano | findstr :8080    # Windows
lsof -i :8080                   # Linux/macOS

# Kill the process or change port in server.py
```

### Permission Issues (Linux/macOS)
```bash
chmod +x setup.sh start.sh start-dev.sh build.sh
```

## 🔒 Security Notes

- API keys are stored in `.env` files (not in code)
- `.env` files are gitignored by default
- CORS headers configured for local development
- No sensitive data transmitted to frontend

## 📄 License

This project is private and not licensed for public use.

## 👥 Credits

- **Neil Bhalla** - Frontend & Integration
- **Geith Amum** - Backend & Architecture

---

**Need help?** Check the troubleshooting section or create an issue in the project repository.