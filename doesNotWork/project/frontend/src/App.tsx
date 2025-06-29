import React, { useState, useRef, useEffect } from 'react';
import { Send, Minus, Square, X, Zap, Bot, User, Calculator, Monitor, Chrome, List, Settings, ArrowLeft, Key, Save, Eye, EyeOff } from 'lucide-react';

declare global {
  interface Window {
    electronAPI?: {
      minimizeWindow: () => Promise<boolean>;
      maximizeWindow: () => Promise<boolean>;
      closeWindow: () => Promise<boolean>;
      ping: () => Promise<string>;
      isElectron: boolean;
      platform: string;
    };
  }
}

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  isCalculation?: boolean;
}

function App() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'available' | 'unavailable'>('checking');
  const [isElectron, setIsElectron] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showApiKeyInput, setShowApiKeyInput] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [isSavingApiKey, setIsSavingApiKey] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const apiKeyInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Detect Electron environment
    const checkElectron = async () => {
      const hasElectronAPI = !!window.electronAPI;
      const hasUserAgent = navigator.userAgent.toLowerCase().includes('electron');
      const hasProcess = typeof window !== 'undefined' && (window as any).process?.type;
      
      const isElectronEnv = hasElectronAPI || hasUserAgent || hasProcess;
      setIsElectron(isElectronEnv);
      
      return isElectronEnv;
    };
    
    checkElectron();
    
    // Check backend status on startup
    setTimeout(() => {
      checkBackendStatus();
    }, 1000);
    
    // Set up periodic status checks
    const statusInterval = setInterval(() => {
      checkBackendStatus();
    }, 10000);
    
    return () => clearInterval(statusInterval);
  }, []);

  useEffect(() => {
    // Auto-focus input when ready
    if (inputRef.current && messages.length === 0) {
      inputRef.current.focus();
    }
  }, [messages.length]);

  useEffect(() => {
    // Scroll to bottom when new messages are added
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-focus API key input when shown
  useEffect(() => {
    if (showApiKeyInput && apiKeyInputRef.current) {
      setTimeout(() => {
        apiKeyInputRef.current?.focus();
      }, 100);
    }
  }, [showApiKeyInput]);

  // Add wheel event listener to ensure scrolling works
  useEffect(() => {
    const chatContainer = chatContainerRef.current;
    if (chatContainer) {
      const handleWheel = (e: WheelEvent) => {
        // Allow default wheel behavior for scrolling
        e.stopPropagation();
      };
      
      chatContainer.addEventListener('wheel', handleWheel, { passive: true });
      
      return () => {
        chatContainer.removeEventListener('wheel', handleWheel);
      };
    }
  }, []);

  const checkBackendStatus = async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      
      const response = await fetch('http://localhost:8080/health', {
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'healthy') {
          setBackendStatus('available');
        } else {
          setBackendStatus('unavailable');
        }
      } else {
        setBackendStatus('unavailable');
      }
    } catch (error) {
      setBackendStatus('unavailable');
    }
  };

  const handleWindowControl = async (action: 'minimize' | 'maximize' | 'close') => {
    // Check if we're in Electron
    if (!window.electronAPI) {
      return;
    }
    
    // Check if the specific function exists
    const functionMap = {
      minimize: window.electronAPI.minimizeWindow,
      maximize: window.electronAPI.maximizeWindow,
      close: window.electronAPI.closeWindow
    };
    
    const targetFunction = functionMap[action];
    if (typeof targetFunction !== 'function') {
      return;
    }
    
    try {
      await targetFunction();
    } catch (error) {
      console.error(`Window ${action} error:`, error);
    }
  };

  const sendToBackend = async (userMessage: string): Promise<string> => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      
      const response = await fetch('http://localhost:8080/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: userMessage }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          setBackendStatus('available');
          return result.result;
        } else {
          setBackendStatus('available');
          return `Error: ${result.error}`;
        }
      } else {
        const errorText = await response.text();
        setBackendStatus('unavailable');
        return `Backend HTTP Error (${response.status}): ${errorText}`;
      }
    } catch (error) {
      setBackendStatus('unavailable');
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          return `Request Timeout: The request took longer than 30 seconds. Please try again.`;
        }
        return `Backend Connection Error: ${error.message}. Make sure the Python backend is running.`;
      }
      return `Unknown Backend Error: ${String(error)}`;
    }
  };

  const saveApiKey = async () => {
    if (!apiKeyInput.trim()) {
      alert('Please enter an API key');
      return;
    }

    if (!apiKeyInput.startsWith('sk-')) {
      alert('OpenAI API keys should start with "sk-". Please check your key.');
      return;
    }

    setIsSavingApiKey(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      const response = await fetch('http://localhost:8080/save-api-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ api_key: apiKeyInput.trim() }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          alert('✅ OpenAI API key saved successfully!\n\nThe backend will now use your API key for requests.');
          setApiKeyInput('');
          setShowApiKeyInput(false);
          setShowSettings(false);
          // Refresh backend status
          setTimeout(() => checkBackendStatus(), 1000);
        } else {
          alert(`Failed to save API key: ${result.error}`);
        }
      } else {
        const errorText = await response.text();
        alert(`Failed to save API key (HTTP ${response.status}): ${errorText}`);
      }
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        alert('Request timeout. Please check if the backend is running and try again.');
      } else {
        alert(`Network error: ${error instanceof Error ? error.message : String(error)}\n\nMake sure the Python backend is running.`);
      }
    } finally {
      setIsSavingApiKey(false);
    }
  };

  const handleQuickAction = async (actionText: string) => {
    // Set the input value and immediately submit
    setInputValue(actionText);
    
    // Create the user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: actionText,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    // Send to backend
    try {
      const responseText = await sendToBackend(userMessage.text);
      
      // Simulate some processing time
      const delay = 500;
      
      setTimeout(() => {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: responseText,
          isUser: false,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, aiResponse]);
        setIsProcessing(false);
      }, delay);
    } catch (error) {
      setTimeout(() => {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: `Unexpected Error: ${error instanceof Error ? error.message : String(error)}`,
          isUser: false,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, aiResponse]);
        setIsProcessing(false);
      }, 500);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue.trim(),
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    // Send to backend
    try {
      const responseText = await sendToBackend(userMessage.text);
      
      // Simulate some processing time
      const delay = 500;
      
      setTimeout(() => {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: responseText,
          isUser: false,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, aiResponse]);
        setIsProcessing(false);
      }, delay);
    } catch (error) {
      setTimeout(() => {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: `Unexpected Error: ${error instanceof Error ? error.message : String(error)}`,
          isUser: false,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, aiResponse]);
        setIsProcessing(false);
      }, 500);
    }
  };

  const getBackendStatusColor = () => {
    switch (backendStatus) {
      case 'available': return 'bg-green-400';
      case 'unavailable': return 'bg-red-400';
      case 'checking': return 'bg-yellow-400';
      default: return 'bg-gray-400';
    }
  };

  const getBackendStatusText = () => {
    switch (backendStatus) {
      case 'available': return 'Connected to OpenAI - ready to help!';
      case 'unavailable': return 'Backend offline - start with "npm run start-backend"';
      case 'checking': return 'Connecting to backend...';
      default: return 'Unknown status';
    }
  };

  const handleBackToHome = () => {
    setMessages([]);
    setShowSettings(false);
    setShowApiKeyInput(false);
  };

  return (
    <div className="h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col overflow-hidden relative">
      {/* Top-left corner: Built with Bolt badge + Back arrow (when in chat) */}
      <div className="fixed top-0 left-0 z-[9998]">
        <div className="flex items-center">
          {/* Back arrow - only show when there are messages */}
          {messages.length > 0 && (
            <button
              onClick={handleBackToHome}
              className="flex items-center justify-center w-10 h-8 bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-sm border-r border-b border-blue-400/30 rounded-br-lg hover:from-blue-500/30 hover:to-purple-500/30 transition-all duration-200 group"
              title="Back to Home"
            >
              <ArrowLeft className="w-4 h-4 text-blue-300 group-hover:text-blue-200 transition-colors" />
            </button>
          )}
          
          {/* Built with Bolt badge */}
          <div className="flex items-center space-x-2 bg-gradient-to-r from-purple-600/20 to-pink-600/20 backdrop-blur-sm border-r border-b border-purple-400/30 rounded-br-lg px-3 py-1.5 shadow-lg">
            <Zap className="w-3 h-3 text-purple-300" />
            <span className="text-xs font-medium text-purple-200 tracking-wide">Built with Bolt</span>
          </div>
        </div>
      </div>

      {/* Window Controls - Flush with top-right corner */}
      <div className="fixed top-0 right-0 z-[9999] flex items-center">
        {/* Minimize Button */}
        <button
          onClick={() => handleWindowControl('minimize')}
          className="w-12 h-8 bg-yellow-500/20 hover:bg-yellow-400/40 transition-all duration-200 flex items-center justify-center group border-l border-b border-yellow-400/40 backdrop-blur-sm"
          title="Minimize"
        >
          <Minus className="w-4 h-4 text-yellow-200 group-hover:text-yellow-100 transition-colors" />
        </button>
        
        {/* Maximize Button */}
        <button
          onClick={() => handleWindowControl('maximize')}
          className="w-12 h-8 bg-green-500/20 hover:bg-green-400/40 transition-all duration-200 flex items-center justify-center group border-l border-b border-green-400/40 backdrop-blur-sm"
          title="Maximize/Restore"
        >
          <Square className="w-3 h-3 text-green-200 group-hover:text-green-100 transition-colors" />
        </button>
        
        {/* Close Button - Red X */}
        <button
          onClick={() => handleWindowControl('close')}
          className="w-12 h-8 bg-red-500/20 hover:bg-red-400/40 transition-all duration-200 flex items-center justify-center group border-b border-red-400/40 backdrop-blur-sm"
          title="Close"
        >
          <X className="w-4 h-4 text-red-200 group-hover:text-red-100 transition-colors" />
        </button>
      </div>

      {/* Settings Button - Only visible on home screen (no messages) */}
      {messages.length === 0 && (
        <div className="fixed top-8 right-0 z-[9998]">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="w-12 h-8 bg-white/10 hover:bg-white/20 transition-all duration-200 flex items-center justify-center group border-l border-b border-white/20 backdrop-blur-sm"
            title="Settings"
          >
            <Settings className="w-4 h-4 text-white/70 group-hover:text-white transition-colors" />
          </button>
        </div>
      )}

      {/* Settings Panel - Only show when on home screen */}
      {showSettings && messages.length === 0 && (
        <div className="fixed top-16 right-4 z-[9997] bg-black/80 backdrop-blur-sm border border-white/20 rounded-lg p-4 shadow-xl min-w-[280px]">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-white font-semibold">Settings</h3>
            <button
              onClick={() => setShowSettings(false)}
              className="text-white/50 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-white/70">Backend Status</span>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${getBackendStatusColor()}`}></div>
                <span className="text-white/60 text-xs">
                  {backendStatus === 'available' ? 'Online' : 
                   backendStatus === 'unavailable' ? 'Offline' : 'Checking'}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-white/70">Environment</span>
              <span className="text-white/60 text-xs">
                {isElectron ? 'Desktop' : 'Browser'}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-white/70">Messages</span>
              <span className="text-white/60 text-xs">{messages.length}</span>
            </div>
            
            <hr className="border-white/20" />
            
            <button
              onClick={() => {
                setMessages([]);
                setShowSettings(false);
              }}
              className="w-full px-3 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded border border-red-400/30 transition-colors text-sm"
            >
              Clear Chat History
            </button>
            
            <button
              onClick={() => {
                setShowApiKeyInput(true);
                setShowSettings(false);
              }}
              className="w-full px-3 py-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-200 rounded border border-blue-400/30 transition-colors text-sm flex items-center justify-center space-x-2"
            >
              <Key className="w-4 h-4" />
              <span>Enter OpenAI API Key</span>
            </button>
          </div>
        </div>
      )}

      {/* API Key Input Modal */}
      {showApiKeyInput && (
        <div className="fixed inset-0 z-[9999] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-white/20 rounded-2xl p-6 shadow-2xl max-w-md w-full">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                  <Key className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-white font-semibold text-lg">OpenAI API Key</h3>
              </div>
              <button
                onClick={() => {
                  setShowApiKeyInput(false);
                  setApiKeyInput('');
                  setShowApiKey(false);
                }}
                className="text-white/50 hover:text-white transition-colors"
                disabled={isSavingApiKey}
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <p className="text-white/70 text-sm mb-3">
                  Enter your OpenAI API key to enable AI responses. Your key will be saved securely in the backend .env file.
                </p>
                
                <div className="relative">
                  <input
                    ref={apiKeyInputRef}
                    type={showApiKey ? 'text' : 'password'}
                    value={apiKeyInput}
                    onChange={(e) => setApiKeyInput(e.target.value)}
                    placeholder="sk-..."
                    disabled={isSavingApiKey}
                    className="w-full bg-white/5 backdrop-blur-sm border border-white/20 rounded-xl px-4 py-3 pr-12 text-white placeholder-white/40 outline-none focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/20 transition-all duration-300 disabled:opacity-50 font-mono text-sm"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        saveApiKey();
                      }
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowApiKey(!showApiKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white/70 transition-colors"
                    disabled={isSavingApiKey}
                  >
                    {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                
                <p className="text-white/50 text-xs mt-2">
                  Get your API key from{' '}
                  <a 
                    href="https://platform.openai.com/api-keys" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 underline"
                  >
                    platform.openai.com/api-keys
                  </a>
                </p>
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={() => {
                    setShowApiKeyInput(false);
                    setApiKeyInput('');
                    setShowApiKey(false);
                  }}
                  disabled={isSavingApiKey}
                  className="flex-1 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-xl border border-white/20 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={saveApiKey}
                  disabled={!apiKeyInput.trim() || isSavingApiKey}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-400 hover:to-purple-400 text-white rounded-xl border border-blue-400/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {isSavingApiKey ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span>Saving...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4" />
                      <span>Save Key</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Welcome Header - Only show when no messages */}
        {messages.length === 0 && (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center">
              <div className="inline-flex items-center space-x-3 mb-6">
                <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-purple-400/20 border border-purple-400/30">
                  <Zap className="w-7 h-7 text-white" />
                </div>
                <h1 className="text-7xl font-black bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent tracking-tight">
                  FIXR
                </h1>
              </div>
              <p className="text-white/70 text-xl mb-2 font-light tracking-wide">
                AI Powered Tech Support
              </p>
              <p className="text-purple-400/80 text-lg mb-10 font-medium">
                What can I help you with?
              </p>
              
              {/* VIBRANT Quick Action Buttons */}
              <div className="grid grid-cols-2 gap-6 max-w-2xl mx-auto">
                {[
                  { 
                    text: 'Fix my slow computer', 
                    icon: Monitor, 
                    gradient: 'from-purple-600 via-purple-500 to-blue-500', 
                    border: 'border-purple-300/60',
                    shadow: 'shadow-purple-500/40',
                    glow: 'shadow-purple-400/30'
                  },
                  { 
                    text: 'Help with coding error', 
                    icon: Calculator, 
                    gradient: 'from-pink-600 via-purple-500 to-indigo-500', 
                    border: 'border-pink-300/60',
                    shadow: 'shadow-pink-500/40',
                    glow: 'shadow-pink-400/30'
                  },
                  { 
                    text: 'Troubleshoot WiFi issues', 
                    icon: Chrome, 
                    gradient: 'from-cyan-500 via-blue-500 to-purple-600', 
                    border: 'border-cyan-300/60',
                    shadow: 'shadow-cyan-500/40',
                    glow: 'shadow-cyan-400/30'
                  },
                  { 
                    text: 'Explain how to backup files', 
                    icon: List, 
                    gradient: 'from-emerald-500 via-teal-500 to-blue-600', 
                    border: 'border-emerald-300/60',
                    shadow: 'shadow-emerald-500/40',
                    glow: 'shadow-emerald-400/30'
                  }
                ].map((action, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickAction(action.text)}
                    disabled={isProcessing}
                    className={`group relative flex items-center space-x-4 px-6 py-5 bg-gradient-to-br ${action.gradient} hover:scale-110 border-2 ${action.border} rounded-2xl text-white text-sm font-semibold transition-all duration-500 backdrop-blur-sm shadow-2xl ${action.shadow} hover:shadow-3xl hover:${action.glow} disabled:opacity-40 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-lg overflow-hidden`}
                  >
                    {/* Animated background glow */}
                    <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"></div>
                    
                    {/* Shimmer effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out"></div>
                    
                    {/* Icon with enhanced styling */}
                    <div className="relative z-10 w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm border border-white/30 group-hover:bg-white/30 transition-all duration-300">
                      <action.icon className="w-5 h-5 text-white drop-shadow-lg" />
                    </div>
                    
                    {/* Text with enhanced styling */}
                    <span className="relative z-10 font-bold tracking-wide text-white drop-shadow-lg group-hover:text-white/95 transition-colors duration-300">
                      {action.text}
                    </span>
                    
                    {/* Pulse animation */}
                    <div className="absolute inset-0 rounded-2xl animate-pulse bg-gradient-to-br from-white/5 to-transparent"></div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Messages Area with Proper Scrolling */}
        {messages.length > 0 && (
          <div 
            ref={chatContainerRef}
            className="flex-1 min-h-0 chat-container"
          >
            <div className="h-full chat-scrollbar">
              <div className="max-w-4xl mx-auto px-6 py-8 space-y-6">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex items-start space-x-4 ${
                      message.isUser ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {!message.isUser && (
                      <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 border border-purple-400/30 shadow-lg">
                        <Bot className="w-5 h-5 text-white" />
                      </div>
                    )}
                    
                    <div className={`flex flex-col ${message.isUser ? 'items-end' : 'items-start'} max-w-2xl`}>
                      <div
                        className={`px-5 py-4 rounded-2xl border backdrop-blur-sm shadow-lg ${
                          message.isUser
                            ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-white border-purple-400/30'
                            : 'bg-white/5 text-white border-white/20'
                        }`}
                      >
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {message.text}
                        </p>
                      </div>
                      <p className="text-xs text-white/40 mt-2 px-2 font-mono">
                        {message.timestamp.toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </p>
                    </div>

                    {message.isUser && (
                      <div className="w-10 h-10 bg-white/10 border border-white/20 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 backdrop-blur-sm">
                        <User className="w-5 h-5 text-white" />
                      </div>
                    )}
                  </div>
                ))}
                
                {isProcessing && (
                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 border border-purple-400/30 rounded-xl flex items-center justify-center mt-1 shadow-lg">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl px-5 py-4 shadow-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
          </div>
        )}

        {/* Input Area - Always at bottom */}
        <div className="border-t border-purple-400/20 bg-black/20 backdrop-blur-sm flex-shrink-0">
          <div className="max-w-4xl mx-auto p-6">
            <form onSubmit={handleSubmit} className="relative">
              <div className="flex items-end space-x-4">
                <div className="flex-1 relative">
                  <textarea
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSubmit(e);
                      }
                    }}
                    placeholder="Ask me anything about tech, coding, troubleshooting..."
                    disabled={isProcessing}
                    rows={1}
                    className="w-full bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl px-5 py-4 text-white placeholder-white/50 outline-none focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all duration-300 resize-none disabled:opacity-50 min-h-[56px] max-h-32 shadow-lg"
                    style={{
                      height: 'auto',
                      minHeight: '56px'
                    }}
                    onInput={(e) => {
                      const target = e.target as HTMLTextAreaElement;
                      target.style.height = 'auto';
                      target.style.height = Math.min(target.scrollHeight, 128) + 'px';
                    }}
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={!inputValue.trim() || isProcessing}
                  className="w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 border border-purple-400/30 rounded-2xl flex items-center justify-center text-white hover:from-purple-400 hover:to-pink-400 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex-shrink-0 shadow-lg hover:shadow-xl"
                >
                  <Send className="w-6 h-6" />
                </button>
              </div>
              
              {/* Status Indicator */}
              <div className="flex items-center justify-center mt-4">
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full ${getBackendStatusColor()} ${backendStatus === 'checking' ? 'animate-pulse' : ''}`}></div>
                  <span className="text-white/50 text-xs font-mono tracking-wide">
                    {isProcessing ? 'Thinking...' : getBackendStatusText()}
                  </span>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Credits - Bottom corners */}
      <div className="absolute bottom-4 left-4 text-white/20 text-xs z-10 font-mono">
        Neil Bhalla
      </div>
      <div className="absolute bottom-4 right-4 text-white/20 text-xs z-10 font-mono">
        Geith Amum
      </div>
    </div>
  );
}

export default App;