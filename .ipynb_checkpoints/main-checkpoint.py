# fixr_graph_ollama_env.py

import os
import subprocess
from typing import TypedDict, Optional
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langchain_community.llms import Ollama
from langchain_community.utilities import SerpAPIWrapper

# Load environment variables from .env file
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Define state schema for LangGraph
class FixrState(TypedDict, total=False):
    user_input: str
    step: str
    diagnosis: Optional[str]
    fix_command: Optional[str]
    fix_result: Optional[str]

# Initialize LLM
llm = Ollama(model=OLLAMA_MODEL)

# Initialize SerpAPI tool
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)

# Shell command execution helper
def run_shell(command: str) -> str:
    try:
        completed = subprocess.run(command, shell=True, capture_output=True, text=True)
        return completed.stdout if completed.stdout else completed.stderr
    except Exception as e:
        return str(e)

tools = {
    "search": Tool(name="search", func=search.run, description="Search the web"),
    "shell": Tool(name="shell", func=run_shell, description="Run a system command"),
}

# LangGraph node functions
def start_node(state: FixrState) -> FixrState:
    print("\n💬 User issue:", state["user_input"])
    return {"step": "diagnose", **state}

def diagnosis_node(state: FixrState) -> FixrState:
    prompt = f"You are a PC tech support assistant. Diagnose the issue: {state['user_input']}. Respond with a fix strategy."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"diagnosis": response.content, "step": "fix", **state}

def fix_node(state: FixrState) -> FixrState:
    prompt = f"Based on the diagnosis: '{state['diagnosis']}', what command should be run to fix it?"
    response = llm.invoke([HumanMessage(content=prompt)])
    command = response.content.strip()

    print(f"\n🛠️ Suggested fix command: {command}")
    result = run_shell(command)
    return {"fix_command": command, "fix_result": result, "step": "done", **state}

def end_node(state: FixrState) -> FixrState:
    print("\n✅ Fix attempted:\n", state["fix_result"])
    return state

# Build LangGraph with state schema
builder = StateGraph(FixrState)

builder.add_node("start", RunnableLambda(start_node))
builder.add_node("diagnose", RunnableLambda(diagnosis_node))
builder.add_node("fix", RunnableLambda(fix_node))
builder.add_node("done", RunnableLambda(end_node))

builder.set_entry_point("start")
builder.add_edge("start", "diagnose")
builder.add_edge("diagnose", "fix")
builder.add_edge("fix", "done")
builder.add_edge("done", END)

graph = builder.compile()

# Run the graph
if __name__ == "__main__":
    user_input = input("Describe your PC issue: ")
    final_state = graph.invoke({"user_input": user_input})
