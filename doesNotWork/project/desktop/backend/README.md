# FIXR Backend - OpenAI Chatbot

A Python backend that integrates with OpenAI's GPT API to provide intelligent responses.

## Setup

### 1. Get OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-`)

### 2. Configure Environment
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and replace `your_openai_api_key_here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### 3. Start the Server
```bash
python server.py
```

## Architecture

- **`server.py`** - HTTP server that handles requests and routing
- **`message.py`** - OpenAI integration and message processing
- **`.env`** - Environment variables (API keys, configuration)

## Files

### server.py (HTTP Server)
Handles all HTTP operations:
- CORS headers
- Request routing
- JSON parsing
- Response formatting
- Delegates message processing to `message.py`

### message.py (OpenAI Integration)
Handles OpenAI API communication:
- Loads environment variables from `.env`
- Sends messages to OpenAI GPT-3.5-turbo
- Handles API errors and timeouts
- Returns formatted responses

### .env (Environment Configuration)
Contains sensitive configuration:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```bash
# Start the server (default port 8080)
python server.py

# Start on custom port
python server.py 3000
```

## API Endpoints

#### GET /health
```bash
curl http://localhost:8080/health
```

#### GET /calculate?expression=<input>
```bash
curl "http://localhost:8080/calculate?expression=How do I fix my WiFi?"
# Response: {"success": true, "result": "Here are some steps to troubleshoot WiFi issues..."}
```

#### POST /calculate
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"expression":"My computer is running slow"}' \
     http://localhost:8080/calculate
# Response: {"success": true, "result": "Here are several ways to speed up your computer..."}
```

## How It Works

1. **Frontend sends message** → `server.py`
2. **Server extracts text** → `server.py`
3. **Message sent to OpenAI** → `message.py`
4. **OpenAI processes with GPT-3.5-turbo** → OpenAI API
5. **Response returned to frontend** → `server.py`

## OpenAI Integration Details

- **Model**: GPT-3.5-turbo (fast and cost-effective)
- **System Prompt**: Configured as "FIXR" tech support assistant
- **Max Tokens**: 1000 (adjustable)
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Timeout**: 60 seconds (1 minute)

## Error Handling

The backend handles various error scenarios:
- Missing or invalid API key
- Network connectivity issues
- OpenAI API rate limits
- Malformed requests
- API timeouts

## Security

- API key stored in `.env` file (not in code)
- `.env` file should be added to `.gitignore`
- CORS headers configured for frontend access
- Request validation and sanitization

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in the `backend/` directory
- Check that the API key is correctly formatted in `.env`
- Ensure no extra spaces around the `=` sign

### "Network Error"
- Check internet connection
- Verify OpenAI API status
- Check firewall/proxy settings

### "OpenAI API Error"
- Verify API key is valid and active
- Check OpenAI account billing/credits
- Review rate limits on your OpenAI account

## Customization

### Change AI Model
Edit `message.py` and modify the `model` parameter:
```python
"model": "gpt-4",  # or "gpt-3.5-turbo-16k"
```

### Adjust Response Length
Modify `max_tokens` in `message.py`:
```python
"max_tokens": 2000,  # Longer responses
```

### Customize System Prompt
Edit the system message in `message.py`:
```python
"content": "You are a specialized coding assistant..."
```

## Cost Considerations

- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Monitor usage in OpenAI dashboard
- Consider implementing rate limiting for production use