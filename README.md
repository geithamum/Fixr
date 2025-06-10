# Claude Agent with LangGraph

This project implements a Claude agent using LangGraph that can interact with Claude's tools like bash and computer_use.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

The agent is configured with two tools:
- `bash`: Execute bash commands in the terminal
- `computer_use`: Use the computer to perform tasks

The agent uses Claude 3 Sonnet to process messages and decide when to use tools. When Claude needs to use a tool, it will format its response with a special `<tool_call>` tag containing the tool name and parameters.

## Example

The example in `main.py` shows how to use the agent to list files in the current directory using the bash tool. You can modify the initial message to test different interactions with the agent.

## Project Structure

- `main.py`: Contains the main implementation of the Claude agent using LangGraph
- `requirements.txt`: Lists all Python dependencies
- `.env`: Contains your Anthropic API key (create this file yourself)

## Note

This is a basic implementation that can be extended with more tools and functionality. The tool execution is currently mocked - you'll need to implement actual tool execution logic for your specific use case. 