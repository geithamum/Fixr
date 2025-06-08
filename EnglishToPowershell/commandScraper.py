#!/usr/bin/env python3
"""
fixr_shell.py

An interactive shell that:
  1. Prompts the user in a PowerShell-like REPL.
  2. If the user input is a request (not a raw command), asks Claude for the appropriate command.
  3. Falls back to web search via SerpAPI when Claude is unsure.
  4. Executes the final PowerShell or cmd command automatically.
  5. Prints stdout and stderr.

Dependencies:
  pip install python-dotenv anthropic serpapi pydantic

Setup:
  - Create a .env file with:
        ANTHROPIC_API_KEY=your_claude_api_key
        SERP_API_KEY=your_serpapi_key

Usage:
  python fixr_shell.py
  Fixr (PowerShell)> bluetooth needs restart
  >> Suggested command to run:
     Restart-Service bthserv -Force
  [shell output...]
  Fixr (PowerShell)> exit
"""

import os
import sys
import subprocess
from dotenv import load_dotenv
import anthropic
from serpapi import GoogleSearch

# ──────────────────────────────────────────────────────
# 1️⃣ Load environment variables
# ──────────────────────────────────────────────────────

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

if not ANTHROPIC_API_KEY:
    print("Error: Please set ANTHROPIC_API_KEY in your .env")
    sys.exit(1)
if not SERP_API_KEY:
    print("Error: Please set SERP_API_KEY in your .env")
    sys.exit(1)

claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# ──────────────────────────────────────────────────────
# 2️⃣ Helper functions
# ──────────────────────────────────────────────────────

def ask_claude_direct(problem: str) -> (str, bool):
    """
    Ask Claude first for a direct command.
    Returns (command, needs_search_flag).
    """
    prompt = (
        f"You are a Windows sysadmin assistant.\n"
        f"The user’s problem: {problem}\n\n"
        "If you are highly confident you know the exact PowerShell or cmd command, reply:\n"
        "COMMAND: <your-command-here>\n\n"
        "Otherwise reply exactly:\n"
        "NEED_EXTERNAL_INFO"
    )
    resp = claude.messages.create(
        model="claude-4-opus-20250514",
        system="You are a helpful assistant.",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=128
    )
    # extract text from TextBlock objects
    text = "".join(getattr(block, "text", "") for block in (resp.content or [])).strip()
    if text.upper().startswith("COMMAND:"):
        return text[len("COMMAND:"):].strip(), False
    return "", True

def web_search_snippets(query: str) -> str:
    """
    Perform a web search and return top 3 snippets concatenated.
    """
    params = {"engine":"google","q":query,"api_key":SERP_API_KEY,"num":3}
    results = GoogleSearch(params).get_dict().get("organic_results", [])
    lines = []
    for r in results:
        title = r.get("title","").strip()
        snippet = r.get("snippet","").strip()
        if title or snippet:
            lines.append(f"{title}: {snippet}")
    return "\n".join(lines)

def ask_claude_with_snippets(problem: str, snippets: str) -> str:
    """
    Ask Claude with search snippets to produce a single command.
    """
    prompt = (
        f"You are a Windows sysadmin assistant.\n"
        f"The user’s problem: {problem}\n\n"
        "Here are some web search results:\n"
        f"{snippets}\n\n"
        "Do NOT copy or quote the snippets. Instead return exactly one "
        "correct PowerShell or cmd command (no extra text) to fix it."
    )
    resp = claude.messages.create(
        model="claude-4-opus-20250514",
        system="You are a helpful assistant.",
        messages=[{"role":"user","content":prompt}],
        max_tokens=128
    )
    return "".join(getattr(block, "text","") for block in (resp.content or [])).strip()

# ──────────────────────────────────────────────────────
# 3️⃣ REPL loop
# ──────────────────────────────────────────────────────

def run_fixr_shell():
    print("Welcome to Fixr Shell. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            user_input = input("Fixr (PowerShell)> ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue

            # Step 1: ask Claude for direct command
            cmd, needs_search = ask_claude_direct(user_input)

            # Step 2: fallback to web search if needed
            if needs_search:
                snippets = web_search_snippets(user_input)
                cmd = ask_claude_with_snippets(user_input, snippets)

            # Show and execute
            print("\n>> Suggested command to run:\n")
            print(cmd, "\n")
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print("[stderr]", result.stderr.strip())

        except KeyboardInterrupt:
            print("\nExiting Fixr Shell.")
            break

if __name__ == "__main__":
    run_fixr_shell()
