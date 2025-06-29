#!/usr/bin/env python3
"""
HTTP server that handles requests and delegates message processing.
"""

import json
import sys
import platform
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import asyncio
import subprocess
import message

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
                result = asyncio.run(message.process_message(params['expression'][0]))
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
                    result = asyncio.run(message.process_message(data['expression']))
                    self.send_json_response({'success': True, 'result': result})
                else:
                    self.send_json_response({'success': False, 'error': 'Missing expression'}, 400)
            except Exception as e:
                self.send_json_response({'success': False, 'error': f"{e}"}, 400)
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
