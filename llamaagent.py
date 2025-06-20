import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOllama
from langchain.memory import ConversationBufferWindowMemory
from langchain.utilities.serpapi import SerpAPIWrapper
import subprocess

# Load environment variables from .env file
load_dotenv()

# Get credentials and settings from env
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi4")

# Memory buffer window
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

# LLM using Ollama
llm = ChatOllama(model=OLLAMA_MODEL)

# SerpAPI tool
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

# Execute shell commands
def execute_command_tool(input: str) -> str:
    try:
        result = subprocess.check_output(input, shell=True, stderr=subprocess.STDOUT, timeout=5)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Define tools
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for answering questions about current events or looking up facts."
    ),
    Tool(
        name="Execute Command",
        func=execute_command_tool,
        description="Executes shell commands. Use with caution."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# Chat loop
def main():
    print("Chat agent is running. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = agent.run(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
