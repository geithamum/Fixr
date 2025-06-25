# FIXR - Cross-Platform Setup Guide

This guide ensures FIXR works perfectly on both Windows and Linux/macOS.

## 🎯 Platform Detection

The setup automatically detects your operating system and uses the appropriate commands:

### Windows
- Uses `.bat` batch files
- Uses `python` command
- Uses Windows-style paths and commands

### Linux/macOS  
- Uses `.sh` shell scripts
- Uses `python3` command
- Uses Unix-style paths and commands

## 📁 File Structure

```
FIXR/
├── Windows Scripts:
│   ├── setup-windows.bat      # Windows setup
│   ├── start-windows.bat      # Windows launcher
│   ├── start-dev-windows.bat  # Windows dev mode
│   └── build-windows.bat      # Windows build
│
├── Linux/macOS Scripts:
│   ├── setup.sh              # Unix setup
│   ├── start.sh              # Unix launcher  
│   ├── start-dev.sh          # Unix dev mode
│   └── build.sh              # Unix build
│
├── Cross-Platform Code:
│   ├── frontend/             # React app (works everywhere)
│   ├── desktop/              # Electron app (cross-platform)
│   ├── backend/              # Python server (cross-platform)
│   └── package.json          # NPM scripts for all platforms
```

## 🚀 Quick Start by Platform

### Windows Users
```cmd
# 1. Setup (one time)
setup-windows.bat

# 2. Add OpenAI key to backend\.env

# 3. Start app
start-windows.bat
```

### Linux/macOS Users
```bash
# 1. Setup (one time)
./setup.sh

# 2. Add OpenAI key to backend/.env

# 3. Start app
./start.sh
```

## 🔧 Cross-Platform Features

### Python Detection
The backend automatically detects the correct Python command:
- **Windows**: `python`
- **Linux/macOS**: `python3`

### Path Handling
- **Windows**: Uses backslashes `\` and Windows paths
- **Linux/macOS**: Uses forward slashes `/` and Unix paths

### File Operations
- **Windows**: Uses Windows batch commands
- **Linux/macOS**: Uses Unix shell commands

### Process Management
- **Windows**: Uses `start` command for background processes
- **Linux/macOS**: Uses `&` for background processes

## 📦 Dependencies

### All Platforms Need:
- **Node.js** v16+ (JavaScript runtime)
- **Python** 3.7+ (Backend server)
- **NPM** (comes with Node.js)

### Platform-Specific Installation:

#### Windows
```cmd
# Install Node.js from nodejs.org
# Install Python from python.org (check "Add to PATH")
```

#### Ubuntu/Debian Linux
```bash
sudo apt update
sudo apt install nodejs npm python3 python3-pip
```

#### CentOS/RHEL Linux
```bash
sudo yum install nodejs npm python3 python3-pip
```

#### macOS
```bash
# Using Homebrew
brew install node python3

# Or download from nodejs.org and python.org
```

## 🛠️ Development Mode

### Windows
```cmd
start-dev-windows.bat
```

### Linux/macOS
```bash
./start-dev.sh
```

Both will:
1. Start Python backend server
2. Start Vite dev server with hot reload
3. Launch Electron app
4. Auto-reload on code changes

## 🏗️ Building Executables

### Windows
```cmd
build-windows.bat
```
Creates: `desktop\dist-electron\FIXR Setup.exe`

### Linux
```bash
./build.sh
```
Creates: `desktop/dist-electron/FIXR-1.0.0.AppImage`

### macOS
```bash
./build.sh
```
Creates: `desktop/dist-electron/FIXR-1.0.0.dmg`

## 🔍 Troubleshooting by Platform

### Windows Issues

#### "python not found"
```cmd
# Install Python from python.org
# Make sure "Add Python to PATH" is checked
# Restart Command Prompt
python --version
```

#### "npm not found"
```cmd
# Install Node.js from nodejs.org
# Restart Command Prompt
node --version
npm --version
```

#### Permission errors
```cmd
# Run Command Prompt as Administrator
# Right-click -> "Run as administrator"
```

### Linux Issues

#### Missing dependencies
```bash
# Ubuntu/Debian
sudo apt install nodejs npm python3 python3-pip

# CentOS/RHEL
sudo yum install nodejs npm python3 python3-pip
```

#### Permission errors
```bash
# Make scripts executable
chmod +x setup.sh start.sh start-dev.sh build.sh

# Or run with bash
bash setup.sh
```

#### Python command not found
```bash
# Install Python 3
sudo apt install python3

# Create symlink if needed
sudo ln -s /usr/bin/python3 /usr/bin/python
```

### macOS Issues

#### Missing Xcode tools
```bash
xcode-select --install
```

#### Homebrew not installed
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Permission issues
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
```

## 🌐 Network Configuration

### Firewall Settings

#### Windows Firewall
1. Open Windows Defender Firewall
2. Allow Python and Node.js through firewall
3. Or temporarily disable for development

#### Linux Firewall (UFW)
```bash
sudo ufw allow 8080
sudo ufw allow 5173
```

#### macOS Firewall
1. System Preferences → Security & Privacy → Firewall
2. Allow Python and Node.js connections

### Port Usage
- **Backend**: Port 8080 (Python server)
- **Frontend Dev**: Port 5173 (Vite dev server)
- **Electron**: Connects to both automatically

## 📊 Performance Notes

### Windows
- Antivirus may slow down Node.js operations
- Windows Defender exclusions recommended for project folder

### Linux
- Generally fastest performance
- May need to increase file watch limits for development

### macOS
- Good performance overall
- May need Rosetta 2 on Apple Silicon Macs

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
# All platforms
npm run install-all

# Or manually
cd frontend && npm update
cd ../desktop && npm update
```

### Cleaning Build Files
```bash
# Windows
rmdir /s /q frontend\dist
rmdir /s /q desktop\dist
rmdir /s /q desktop\dist-electron

# Linux/macOS
rm -rf frontend/dist
rm -rf desktop/dist  
rm -rf desktop/dist-electron
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend starts: `http://localhost:8080/health`
- [ ] Frontend builds: Check `frontend/dist/` folder
- [ ] Desktop app launches: Window opens with FIXR interface
- [ ] OpenAI integration: Send a test message
- [ ] Window controls: Minimize/maximize/close work

## 🆘 Getting Help

If you encounter platform-specific issues:

1. **Check the logs**: Look for error messages in terminal
2. **Verify prerequisites**: Node.js, Python, npm versions
3. **Check permissions**: File/folder access rights
4. **Review firewall**: Network connectivity
5. **Platform-specific forums**: Stack Overflow, GitHub Issues

---

This cross-platform setup ensures FIXR works seamlessly on Windows, Linux, and macOS with minimal configuration differences.