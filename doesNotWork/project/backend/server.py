#!/usr/bin/env python3
"""
HTTP server that handles requests and delegates message processing.
"""

import json
import sys
import platform
import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from message import process_message

class ServerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json_response({'status': 'healthy'})
        elif self.path.startswith('/calculate?'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            if 'expression' in params:
                result = asyncio.get_event_loop().run_until_complete(process_message(params['expression'][0]))
                self.send_json_response({'success': True, 'result': result})
            else:
                self.send_json_response({'success': False, 'error': 'Missing expression'}, 400)
        else:
            self.send_json_response({'success': False, 'error': 'Not found'}, 404)
    
    def do_POST(self):
        if self.path == '/calculate':
            try:
                content_length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(content_length).decode('utf-8'))
                if 'expression' in data:
                    result = asyncio.get_event_loop().run_until_complete(process_message(data['expression']))
                    self.send_json_response({'success': True, 'result': result})
                else:
                    self.send_json_response({'success': False, 'error': 'Missing expression'}, 400)
            except:
                self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
        elif self.path == '/save-api-key':
            try:
                content_length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(content_length).decode('utf-8'))
                
                if 'api_key' not in data:
                    self.send_json_response({'success': False, 'error': 'Missing api_key'}, 400)
                    return
                
                api_key = data['api_key'].strip()
                
                if not api_key:
                    self.send_json_response({'success': False, 'error': 'API key cannot be empty'}, 400)
                    return
                
                if not api_key.startswith('sk-'):
                    self.send_json_response({'success': False, 'error': 'Invalid API key format. OpenAI keys start with "sk-"'}, 400)
                    return
                
                # Save API key to .env file
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                
                try:
                    # Read existing .env content
                    env_content = []
                    if os.path.exists(env_path):
                        with open(env_path, 'r') as f:
                            env_content = f.readlines()
                    
                    # Update or add the API key line
                    api_key_line = f'OPENAI_API_KEY={api_key}\n'
                    updated = False
                    
                    for i, line in enumerate(env_content):
                        if line.strip().startswith('OPENAI_API_KEY='):
                            env_content[i] = api_key_line
                            updated = True
                            break
                    
                    if not updated:
                        env_content.append(api_key_line)
                    
                    # Write back to .env file
                    with open(env_path, 'w') as f:
                        f.writelines(env_content)
                    
                    print(f"✅ API key saved to {env_path}")
                    self.send_json_response({'success': True, 'message': 'API key saved successfully'})
                    
                except Exception as e:
                    print(f"❌ Error saving API key: {e}")
                    self.send_json_response({'success': False, 'error': f'Failed to save API key: {str(e)}'}, 500)
                    
            except json.JSONDecodeError:
                self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
            except Exception as e:
                print(f"❌ Unexpected error in /save-api-key: {e}")
                self.send_json_response({'success': False, 'error': f'Server error: {str(e)}'}, 500)
        else:
            self.send_json_response({'success': False, 'error': 'Not found'}, 404)
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(('', port), ServerHandler)
    
    # Detect platform and show appropriate instructions
    system = platform.system()
    if system == "Windows":
        python_cmd = "python"
    else:
        python_cmd = "python3"
    
    print(f"FIXR Backend Server starting on port {port}")
    print(f"Platform: {system}")
    print(f"Python: {sys.version}")
    print(f"Server URL: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        server.shutdown()