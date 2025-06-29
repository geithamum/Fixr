import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Window controls
  minimizeWindow: () => {
    console.log('🔧 Preload: Minimize window called');
    return ipcRenderer.invoke('window-minimize');
  },
  maximizeWindow: () => {
    console.log('🔧 Preload: Maximize window called');
    return ipcRenderer.invoke('window-maximize');
  },
  closeWindow: () => {
    console.log('🔧 Preload: Close window called');
    return ipcRenderer.invoke('window-close');
  },
  
  // Debug function
  ping: () => {
    console.log('🔧 Preload: Ping called');
    return ipcRenderer.invoke('ping');
  },
  
  // Check if we're in Electron
  isElectron: true,
  
  // Platform info
  platform: process.platform
});

// Debug: Log when preload script loads
console.log('🔧 Preload script loaded successfully');
console.log('🔧 electronAPI exposed to window object');

// Test IPC connection on load
window.addEventListener('DOMContentLoaded', () => {
  console.log('🔧 DOM loaded, testing IPC connection...');
  ipcRenderer.invoke('ping').then(response => {
    console.log('🔧 IPC test successful:', response);
  }).catch(error => {
    console.error('🔧 IPC test failed:', error);
  });
});