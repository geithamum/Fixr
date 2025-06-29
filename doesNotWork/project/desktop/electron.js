import { app, BrowserWindow, ipcMain, shell } from 'electron';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync } from 'fs';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const isDev = process.env.NODE_ENV === 'development';

let mainWindow;
let backendProcess = null;

// Function to start Python backend
function startPythonBackend() {
  console.log('🐍 Starting Python backend...');
  
  // Determine Python command based on platform
  const isWindows = process.platform === 'win32';
  const pythonCmd = isWindows ? 'python' : 'python3';
  
  // FIXED: Better path resolution for packaged app
  let backendPath;
  let serverPath;
  
  if (isDev) {
    // Development mode
    backendPath = join(__dirname, '../backend');
    serverPath = join(backendPath, 'server.py');
  } else {
    // Production mode - backend is in resources
    if (process.resourcesPath) {
      // Standard packaged app
      backendPath = join(process.resourcesPath, 'backend');
      serverPath = join(backendPath, 'server.py');
    } else {
      // Portable app fallback
      backendPath = join(process.cwd(), 'resources', 'backend');
      serverPath = join(backendPath, 'server.py');
      
      // If that doesn't exist, try relative to executable
      if (!existsSync(serverPath)) {
        backendPath = join(__dirname, 'backend');
        serverPath = join(backendPath, 'server.py');
      }
    }
  }
  
  console.log('🔍 Backend path:', backendPath);
  console.log('🔍 Server script:', serverPath);
  console.log('🔍 Python command:', pythonCmd);
  console.log('🔍 Is packaged app:', !isDev);
  console.log('🔍 Process resourcesPath:', process.resourcesPath);
  console.log('🔍 Process cwd:', process.cwd());
  console.log('🔍 __dirname:', __dirname);
  
  // Check if server.py exists
  if (!existsSync(serverPath)) {
    console.error('❌ server.py not found at:', serverPath);
    
    // Try multiple fallback paths for packaged app
    const fallbackPaths = [
      join(__dirname, 'backend', 'server.py'),
      join(__dirname, '../backend/server.py'),
      join(process.cwd(), 'backend', 'server.py'),
      join(app.getAppPath(), 'backend', 'server.py'),
      join(app.getAppPath(), '../backend/server.py')
    ];
    
    for (const fallbackPath of fallbackPaths) {
      console.log('🔍 Trying fallback path:', fallbackPath);
      if (existsSync(fallbackPath)) {
        console.log('✅ Found backend at fallback:', fallbackPath);
        backendPath = dirname(fallbackPath);
        serverPath = fallbackPath;
        break;
      }
    }
    
    if (!existsSync(serverPath)) {
      console.error('❌ Backend not found in any expected location');
      return false;
    }
  }
  
  return startPythonFromPath(pythonCmd, backendPath, serverPath);
}

function startPythonFromPath(pythonCmd, backendPath, serverPath) {
  try {
    // Spawn Python process with better error handling
    const spawnOptions = {
      cwd: backendPath,
      stdio: ['pipe', 'pipe', 'pipe'],
      detached: false,
      windowsHide: true, // Hide console window on Windows
      env: { 
        ...process.env, 
        PYTHONUNBUFFERED: '1',
        PYTHONPATH: backendPath // Ensure Python can find modules
      }
    };
    
    console.log('🚀 Spawning Python with options:', { 
      cmd: pythonCmd, 
      args: ['server.py'],
      cwd: backendPath 
    });
    
    const serverExe = path.join(backendPath, 'server.exe');
    backendProcess = spawn(serverExe, [], {
      cwd: backendPath,
      detached: true,
      stdio: 'ignore', // or 'inherit' to debug
      windowsHide: true
    });

    backendProcess.unref();

    
    if (!backendProcess || !backendProcess.pid) {
      console.error('❌ Failed to spawn Python process');
      return false;
    }
    
    console.log('🚀 Backend process started with PID:', backendProcess.pid);
    
    // Handle backend output with better logging
    backendProcess.stdout.on('data', (data) => {
      const output = data.toString().trim();
      if (output) {
        console.log('🐍 Backend stdout:', output);
        
        // Check for successful startup messages
        if (output.includes('starting on port') || output.includes('Server URL')) {
          console.log('✅ Backend server started successfully');
        }
      }
    });
    
    backendProcess.stderr.on('data', (data) => {
      const error = data.toString().trim();
      if (error && !error.includes('WARNING') && !error.toLowerCase().includes('deprecation')) {
        console.error('🐍 Backend stderr:', error);
      }
    });
    
    // Handle backend process exit
    backendProcess.on('exit', (code, signal) => {
      console.log(`🐍 Backend process exited with code ${code}, signal ${signal}`);
      backendProcess = null;
      
      // Try to restart backend if it crashes unexpectedly
      if (code !== 0 && code !== null && !isDev) {
        console.log('🔄 Backend crashed, attempting restart in 5 seconds...');
        setTimeout(() => {
          if (!backendProcess) {
            startPythonBackend();
          }
        }, 5000);
      }
    });
    
    backendProcess.on('error', (error) => {
      console.error('🐍 Backend process error:', error.message);
      
      // Try alternative Python commands
      if (error.code === 'ENOENT') {
        console.log('🔄 Trying alternative Python commands...');
        const altCommands = process.platform === 'win32' 
          ? ['py', 'python3', 'python.exe']
          : ['python3', 'python', 'python3.11', 'python3.10'];
        
        for (const altCmd of altCommands) {
          if (altCmd !== pythonCmd) {
            console.log(`🔄 Trying ${altCmd}...`);
            try {
              const altOptions = { ...spawnOptions };
              backendProcess = spawn(altCmd, ['server.py'], altOptions);
              if (backendProcess && backendProcess.pid) {
                console.log(`✅ Backend started with ${altCmd}, PID:`, backendProcess.pid);
                return true;
              }
            } catch (e) {
              console.log(`❌ ${altCmd} failed:`, e.message);
            }
          }
        }
      }
      
      backendProcess = null;
    });
    
    return true;
  } catch (error) {
    console.error('🐍 Error starting backend:', error.message);
    return false;
  }
}

// Function to stop Python backend
function stopPythonBackend() {
  if (backendProcess) {
    console.log('🛑 Stopping Python backend...');
    
    try {
      // Try graceful shutdown first
      if (process.platform === 'win32') {
        // On Windows, use taskkill for better process termination
        spawn('taskkill', ['/pid', backendProcess.pid.toString(), '/f', '/t'], {
          stdio: 'ignore'
        });
      } else {
        // On Unix systems, send SIGTERM
        backendProcess.kill('SIGTERM');
      }
      
      // Force kill after 5 seconds if still running
      setTimeout(() => {
        if (backendProcess && !backendProcess.killed) {
          console.log('🔥 Force killing backend process...');
          backendProcess.kill('SIGKILL');
        }
      }, 5000);
      
    } catch (error) {
      console.error('🛑 Error stopping backend:', error.message);
    }
    
    backendProcess = null;
  }
}

function createWindow() {
  // Create app icon path
  const iconPath = join(__dirname, 'assets', 'icon.png');
  const iconExists = existsSync(iconPath);
  
  console.log('🎨 Icon path:', iconPath);
  console.log('🎨 Icon exists:', iconExists);
  
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: join(__dirname, 'preload.js'),
      webSecurity: false // Allow loading local files
    },
    titleBarStyle: 'hidden', // Better Windows compatibility
    frame: false,
    backgroundColor: '#0f0f23',
    show: false,
    icon: iconExists ? iconPath : undefined // Use icon if it exists
  });

  // Start Python backend before loading the UI
  console.log('🚀 Starting backend before UI load...');
  const backendStarted = startPythonBackend();
  
  if (backendStarted) {
    console.log('✅ Backend startup initiated');
    // Give backend more time to start before loading UI
    setTimeout(() => {
      loadMainWindow();
    }, 4000); // Increased from 3000 to 4000ms for packaged apps
  } else {
    console.log('⚠️ Backend failed to start, loading UI anyway');
    setTimeout(() => {
      loadMainWindow();
    }, 1000);
  }
  
  function loadMainWindow() {
    // Determine what to load
    if (isDev) {
      // Development mode - load from Vite dev server
      console.log('🔧 Development mode: Loading from Vite dev server');
      mainWindow.loadURL('http://localhost:5173');
      mainWindow.webContents.openDevTools();
    } else {
      // Production mode - load from built files
      const indexPath = join(__dirname, 'dist/index.html');
      console.log('📦 Production mode: Loading from', indexPath);
      
      if (existsSync(indexPath)) {
        mainWindow.loadFile(indexPath);
        console.log('✅ Successfully loaded index.html');
      } else {
        console.error('❌ index.html not found at:', indexPath);
        
        // Fallback: create a simple error page
        const errorHtml = `
          <!DOCTYPE html>
          <html>
          <head>
            <title>FIXR - Setup Required</title>
            <style>
              body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                height: 100vh; 
                margin: 0;
                text-align: center;
              }
              .container { 
                background: rgba(0,0,0,0.3); 
                padding: 40px; 
                border-radius: 20px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
              }
              h1 { color: #ff6b6b; margin-bottom: 20px; }
              .steps { text-align: left; margin: 20px 0; }
              .step { margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px; }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>⚠️ FIXR Setup Required</h1>
              <p>The frontend files are not built yet.</p>
              <div class="steps">
                <div class="step">1. Close this window</div>
                <div class="step">2. Run: <code>BUILD-EXE.bat</code></div>
                <div class="step">3. Use the generated executable</div>
              </div>
              <p>This will build the frontend and create a proper executable.</p>
              <p><strong>Backend Status:</strong> ${backendStarted ? '✅ Running' : '❌ Failed to start'}</p>
            </div>
          </body>
          </html>
        `;
        
        mainWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(errorHtml)}`);
      }
    }
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    if (isDev) {
      console.log('🚀 FIXR Desktop ready in development mode!');
      console.log('🔧 Frontend: http://localhost:5173');
    } else {
      console.log('🚀 FIXR Desktop ready!');
    }
    
    if (backendProcess && backendProcess.pid) {
      console.log('🐍 Backend running on: http://localhost:8080');
      console.log('🐍 Backend PID:', backendProcess.pid);
    } else {
      console.log('⚠️ Backend not running - some features may not work');
    }
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Handle app closing - make sure to stop backend
  mainWindow.on('closed', () => {
    console.log('🪟 Main window closed');
    stopPythonBackend();
    mainWindow = null;
  });

  // Debug: Log when page finishes loading
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('✓ Page finished loading');
  });

  // Debug: Log any load failures
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
    console.error('❌ Page failed to load:', errorDescription, 'URL:', validatedURL);
  });
}

// Handle window controls via IPC
ipcMain.handle('window-minimize', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.minimize();
    return true;
  }
  return false;
});

ipcMain.handle('window-maximize', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
    return true;
  }
  return false;
});

ipcMain.handle('window-close', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.close();
    return true;
  }
  return false;
});

// Additional IPC handlers
ipcMain.handle('ping', () => {
  return 'pong';
});

// Backend status check
ipcMain.handle('backend-status', () => {
  return {
    running: backendProcess !== null && !backendProcess.killed,
    pid: backendProcess ? backendProcess.pid : null
  };
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  console.log('🚪 All windows closed');
  stopPythonBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Handle app quit - ensure backend is stopped
app.on('before-quit', (event) => {
  console.log('🚪 App is quitting...');
  if (backendProcess) {
    console.log('⏳ Stopping backend before quit...');
    stopPythonBackend();
  }
});

app.on('will-quit', (event) => {
  console.log('🚪 App will quit...');
  if (backendProcess) {
    console.log('⏳ Waiting for backend to stop...');
    event.preventDefault();
    
    // Give backend time to stop gracefully
    setTimeout(() => {
      stopPythonBackend();
      app.quit();
    }, 1000);
  }
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('🚨 Uncaught Exception:', error);
  stopPythonBackend();
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('🚨 Unhandled Rejection at:', promise, 'reason:', reason);
});