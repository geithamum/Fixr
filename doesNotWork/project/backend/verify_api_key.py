#!/usr/bin/env python3
"""
OpenAI API Key Verification Script
Validates an API key by making a test request to OpenAI
"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def verify_openai_api_key(api_key):
    """
    Verify an OpenAI API key by making a test request
    Returns: (is_valid: bool, message: str, details: dict)
    """
    
    # Basic format validation
    if not api_key:
        return False, "API key is empty", {}
    
    if not api_key.startswith('sk-'):
        return False, "Invalid API key format. OpenAI API keys start with 'sk-'", {}
    
    if len(api_key) < 20:
        return False, "API key is too short", {}
    
    try:
        # Make a minimal test request to OpenAI API
        url = "https://api.openai.com/v1/models"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'FIXR-API-Verification/1.0'
        }
        
        # Create and send the request with 10-second timeout
        request = Request(url, headers=headers)
        
        with urlopen(request, timeout=10) as response:
            if response.status == 200:
                response_data = json.loads(response.read().decode('utf-8'))
                
                # Check if we got a valid models response
                if 'data' in response_data and isinstance(response_data['data'], list):
                    model_count = len(response_data['data'])
                    return True, f"API key is valid! Found {model_count} available models.", {
                        'model_count': model_count,
                        'has_gpt35': any('gpt-3.5' in model.get('id', '') for model in response_data['data']),
                        'has_gpt4': any('gpt-4' in model.get('id', '') for model in response_data['data'])
                    }
                else:
                    return False, "Unexpected response format from OpenAI API", {}
            else:
                return False, f"OpenAI API returned status code {response.status}", {}
                
    except HTTPError as e:
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        try:
            error_data = json.loads(error_body)
            error_message = error_data.get('error', {}).get('message', 'Unknown API error')
            
            # Handle specific error types
            if 'invalid_api_key' in error_message.lower() or 'incorrect api key' in error_message.lower():
                return False, "Invalid API key. Please check your key and try again.", {'error_type': 'invalid_key'}
            elif 'insufficient_quota' in error_message.lower():
                return False, "API key is valid but you've exceeded your quota. Please check your billing.", {'error_type': 'quota_exceeded'}
            elif 'rate_limit' in error_message.lower():
                return False, "API key is valid but rate limited. Please wait and try again.", {'error_type': 'rate_limited'}
            else:
                return False, f"OpenAI API Error: {error_message}", {'error_type': 'api_error'}
        except:
            return False, f"OpenAI API Error: HTTP {e.code}", {'error_type': 'http_error'}
            
    except URLError as e:
        return False, f"Network Error: Unable to connect to OpenAI API. Check your internet connection.", {'error_type': 'network_error'}
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON response from OpenAI API", {'error_type': 'json_error'}
        
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}", {'error_type': 'unknown_error'}

def main():
    """
    Main function for command-line usage
    """
    if len(sys.argv) != 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python verify_api_key.py <api_key>'
        }))
        sys.exit(1)
    
    api_key = sys.argv[1].strip()
    is_valid, message, details = verify_openai_api_key(api_key)
    
    result = {
        'success': is_valid,
        'message': message,
        'details': details
    }
    
    print(json.dumps(result))
    sys.exit(0 if is_valid else 1)

if __name__ == '__main__':
    main()