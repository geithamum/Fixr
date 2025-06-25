import { app, BrowserWindow, ipcMain, shell } from 'electron';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const isDev = process.env.NODE_ENV === 'development';

let mainWindow;

function createWindow() {
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
    titleBarStyle: 'hiddenInset',
    frame: false,
    backgroundColor: '#0f0f23',
    show: false,
    icon: join(__dirname, '../assets/icon.png')
  });

  // Determine what to load
  if (isDev) {
    // Development mode - load from Vite dev server
    console.log('🔧 Development mode: Loading from Vite dev server');
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // Production mode - load from built files
    const indexPath = join(__dirname, '../dist/index.html');
    console.log('📦 Production mode: Loading from', indexPath);
    
    if (existsSync(indexPath)) {
      mainWindow.loadFile(indexPath);
      console.log('✓ Successfully loaded index.html');
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
              <div class="step">2. Run: <code>setup-windows.bat</code></div>
              <div class="step">3. Run: <code>start-windows.bat</code></div>
            </div>
            <p>This will build the frontend and start the app properly.</p>
          </div>
        </body>
        </html>
      `;
      
      mainWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(errorHtml)}`);
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
    console.log('🐍 Backend should be running on: http://localhost:8080');
    console.log('💡 If backend is not running, the app will show "Backend offline" status');
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Handle app closing
  mainWindow.on('closed', () => {
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
ipcMain.handle('minimize-window', () => {
  if (mainWindow) {
    mainWindow.minimize();
    return true;
  }
  return false;
});

ipcMain.handle('maximize-window', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
    return true;
  }
  return false;
});

ipcMain.handle('close-window', () => {
  if (mainWindow) {
    mainWindow.close();
    return true;
  }
  return false;
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Handle app updates and security
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
    shell.openExternal(navigationUrl);
  });
});