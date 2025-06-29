import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def process_message(input_text):
    """Send message to OpenAI and return the response"""
    # Load environment variables
    load_env()
    
    # Get API key from environment
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        return "Error: OPENAI_API_KEY not found. Please set up your OpenAI API key in the application."
    
    if api_key == 'your_openai_api_key_here':
        return "Error: Please replace the placeholder API key with your actual OpenAI API key."
    
    if not input_text.strip():
        return "Error: Empty message received."
    
    try:
        # Prepare the request to OpenAI API
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are FIXR, an AI assistant that specializes in tech support, troubleshooting, and problem-solving. You help users with computer issues, software problems, coding questions, and general technology guidance. Be helpful, clear, and provide step-by-step solutions when appropriate. Keep responses concise but thorough."
                },
                {
                    "role": "user", 
                    "content": input_text
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # Create and send the request with 60-second timeout
        request = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        
        with urlopen(request, timeout=60) as response:
            if response.status == 200:
                response_data = json.loads(response.read().decode('utf-8'))
                
                # Extract the assistant's message
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    message = response_data['choices'][0]['message']['content']
                    return message.strip()
                else:
                    return "Error: Unexpected response format from OpenAI API."
            else:
                return f"Error: OpenAI API returned status code {response.status}"
                
    except HTTPError as e:
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        try:
            error_data = json.loads(error_body)
            error_message = error_data.get('error', {}).get('message', 'Unknown API error')
            
            # Handle specific error types
            if 'invalid_api_key' in error_message.lower():
                return "Error: Invalid OpenAI API key. Please check your API key and try again."
            elif 'insufficient_quota' in error_message.lower():
                return "Error: OpenAI API quota exceeded. Please check your billing and usage limits."
            elif 'rate_limit' in error_message.lower():
                return "Error: Rate limit exceeded. Please wait a moment and try again."
            else:
                return f"OpenAI API Error: {error_message}"
        except:
            return f"OpenAI API Error: HTTP {e.code} - {error_body}"
            
    except URLError as e:
        return f"Network Error: Unable to connect to OpenAI API. Check your internet connection. ({str(e)})"
        
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON response from OpenAI API. ({str(e)})"
        
    except Exception as e:
        return f"Unexpected Error: {str(e)}"