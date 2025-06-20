import os
import subprocess
from dotenv import load_dotenv

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.utilities import SerpAPIWrapper
from langchain_anthropic import ChatAnthropic
from langchain.agents.agent import AgentExecutor

# Load .env variables
load_dotenv()

# Claude LLM
llm = ChatAnthropic(
    model="claude-opus-4-20250514",
    temperature=0.7,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Web search
search = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY")
)

# Local shell command tool
def run_shell_command(input_text: str) -> str:
    try:
        output = subprocess.check_output(input_text, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.output.decode()}"
    except Exception as e:
        return str(e)

# Tool list
tools = [
    Tool(
        name="Web Search",
        func=search.run,
        description="Useful for answering questions about current events or general knowledge"
    ),
    Tool(
        name="Command Executor",
        func=run_shell_command,
        description="""Executes shell commands on the local machine.
        If the user asks to open/run/launch/execute a program, do it using a command.
        If the user asks to open a file, do it using a command.
        If the user asks to open a folder, do it using a command.
        If the user asks to open a website, do it using a command.
        If the user asks to open a document, do it using a command.
        If the user asks to open a spreadsheet, do it using a command.
        If the user asks to open a presentation, do it using a command.
        """
    )
]

# Memory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5,
)

# 🧠 System prompt
system_prompt = """
You are Fixr, an AI technical assistant that helps users troubleshoot, search, and operate their computer.
- You are concise, technical, and precise.
- Use available tools to run commands or search the web before replying when appropriate.
- If a user asks to open or run something, try to find it or execute a command.
- Think step by step and avoid making assumptions.

SYSTEM INFO:
- You are running on a Windows 11 machine.


"""

# Agent setup
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "system_message": system_prompt
    }
)

# CLI loop
if __name__ == "__main__":
    print("Fixr AI Assistant (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = agent_executor.run(user_input)
        print("Fixr:", response)
