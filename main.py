from typing import Dict, TypedDict, List
from langgraph.graph import Graph, StateGraph
from pydantic import BaseModel
import json
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define the tools available to Claude
TOOLS = [
    {
        "name": "bash",
        "description": "Execute bash commands in the terminal",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "computer_use",
        "description": "Use the computer to perform tasks",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "The action to perform"
                }
            },
            "required": ["action"]
        }
    }
]

# Define the state schema
class AgentState(TypedDict):
    messages: List[Dict]
    next: str

# Function to generate Claude's response
def get_claude_response(state: AgentState) -> AgentState:
    print("Entering get_claude_response with state:", state)  # Debug print
    messages = state["messages"]
    
    # Prepare the messages for Claude
    claude_messages = []
    for msg in messages:
        if msg["role"] == "user":
            claude_messages.append({"role": "user", "content": msg["content"].strip()})
        elif msg["role"] == "assistant":
            claude_messages.append({"role": "assistant", "content": msg["content"].strip()})
        elif msg["role"] == "tool":
            # Add tool results as assistant messages with context
            claude_messages.append({"role": "assistant", "content": f"Tool execution result: {msg['content'].strip()}"})
    
    # Get response from Claude
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        messages=claude_messages,
        temperature=0,
        system=f"""You are a helpful AI assistant with access to the following tools:
{json.dumps(TOOLS, indent=2)}

When you need to use a tool, format your response as:
<tool_call>
{{"name": "tool_name", "parameters": {{"param1": "value1"}}}}
</tool_call>

Important: When running commands on Windows, use Windows-compatible commands:
- Use 'dir' instead of 'ls' for listing files
- Use 'type' instead of 'cat' for viewing files
- Use 'del' instead of 'rm' for deleting files
- Use 'md' or 'mkdir' instead of 'mkdir' for creating directories
- Use 'rd' or 'rmdir' instead of 'rmdir' for removing directories

Otherwise, respond normally to help the user.""".strip()
    )
    
    # Add Claude's response to messages
    messages.append({"role": "assistant", "content": response.content[0].text.strip()})
    
    # Check if the response contains a tool call
    if "<tool_call>" in response.content[0].text:
        state["next"] = "execute_tool"
    else:
        state["next"] = "end"
    
    print("Exiting get_claude_response with state:", state)  # Debug print
    return state

# Function to execute tools
def execute_tool(state: AgentState) -> AgentState:
    print("Entering execute_tool with state:", state)  # Debug print
    last_message = state["messages"][-1]["content"]
    
    # Extract tool call from the message
    start_idx = last_message.find("<tool_call>")
    end_idx = last_message.find("</tool_call>")
    
    if start_idx != -1 and end_idx != -1:
        tool_call = json.loads(last_message[start_idx + 11:end_idx].strip())
        tool_name = tool_call["name"]
        parameters = tool_call["parameters"]
        
        try:
            if tool_name == "bash":
                import subprocess
                import platform
                
                command = parameters["command"]
                
                # Determine the shell to use based on the platform
                if platform.system() == "Windows":
                    shell = True  # Use cmd.exe on Windows
                else:
                    shell = False  # Use direct command execution on Unix-like systems
                
                # Execute the command
                process = subprocess.run(
                    command,
                    shell=shell,
                    capture_output=True,
                    text=True,
                    timeout=30  # Add a timeout for safety
                )
                
                # Prepare the result
                if process.returncode == 0:
                    tool_result = process.stdout.strip()
                else:
                    tool_result = f"Error executing command:\nStdout: {process.stdout.strip()}\nStderr: {process.stderr.strip()}"
            
            elif tool_name == "computer_use":
                import os
                import shutil
                
                action = parameters["action"].strip()
                
                if action.startswith("list_directory"):
                    # List directory contents
                    path = "." if len(action.split()) == 1 else action.split(maxsplit=1)[1]
                    files = os.listdir(path)
                    tool_result = "\n".join(files).strip()
                
                elif action.startswith("get_cwd"):
                    # Get current working directory
                    tool_result = os.getcwd().strip()
                
                elif action.startswith("disk_usage"):
                    # Get disk usage for current directory
                    usage = shutil.disk_usage(".")
                    tool_result = f"Total: {usage.total // (2**30)} GB\nUsed: {usage.used // (2**30)} GB\nFree: {usage.free // (2**30)} GB".strip()
                
                else:
                    tool_result = f"Unsupported computer_use action: {action}".strip()
            
            else:
                tool_result = f"Unknown tool: {tool_name}".strip()
        
        except Exception as e:
            tool_result = f"Error executing {tool_name}: {str(e)}".strip()
        
        # Add tool result to messages
        state["messages"].append({"role": "tool", "content": tool_result})
        state["next"] = "get_claude_response"
    
    print("Exiting execute_tool with state:", state)  # Debug print
    return state

# Add an end node function
def end_node(state: AgentState) -> AgentState:
    """End node that marks the completion of the conversation."""
    print("Entering end_node with state:", state)  # Debug print
    return state

# Create the graph
def create_agent() -> Graph:
    # Create workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("get_claude_response", get_claude_response)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("end", end_node)
    
    # Add edges
    workflow.add_edge("get_claude_response", "execute_tool")
    workflow.add_edge("execute_tool", "get_claude_response")
    
    # Set entry point
    workflow.set_entry_point("get_claude_response")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "get_claude_response",
        lambda x: x["next"],
        {
            "execute_tool": "execute_tool",
            "end": "end"
        }
    )
    
    return workflow.compile()

# Example usage
if __name__ == "__main__":
    # Create the agent
    agent = create_agent()
    
    # Initialize state with a starting message
    initial_state = {
        "messages": [
            {"role": "user", "content": "Please list the files in the current directory using the bash tool."}
        ],
        "next": "get_claude_response"
    }
    
    print("Initial state:", initial_state)  # Debug print
    
    try:
        # Run the agent
        for state in agent.stream(initial_state):
            print("\nReceived state in stream:", state)  # Debug print
            
            # Get the actual state from the nested structure
            current_node = next(iter(state))  # Get the first (and only) key
            current_state = state[current_node]
            
            print("\nCurrent messages:")
            for message in current_state["messages"]:
                print(f"{message['role']}: {message['content']}")
                
            # If we've reached the end state, break
            if current_state["next"] == "end":
                break
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        print("Current state when error occurred:", state if 'state' in locals() else "State not available")
