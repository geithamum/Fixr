import asyncio
import json
import subprocess
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from .cache import PromptCache

def ask_ollama(prompt, model="phi4"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

def run_command(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
        print(f"✔️ Ran: {cmd}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    user_input = input("🧠 What do you want Fixr to do? > ")
    ollama_prompt = f"Write a Windows command to: {user_input}\nOnly output the CMD command."
    command = ask_ollama(ollama_prompt).strip()
    print(f"💻 Generated Command:\n{command}")
    confirm = input("Run this command? (y/n): ")
    if confirm.lower().startswith("y"):
        run_command(command)

class OllamaLLM:
    """Ollama language model interface"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.cache = PromptCache()
        self.logger = logging.getLogger(__name__)
    
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Ollama"""
        try:
            full_prompt = f"{context}\n\nUser: {prompt}\n\nAssistant:"
            
            # Try to get response from cache first
            cached_response = self.cache.get(full_prompt)
            if cached_response is not None:
                self.logger.info("Cache hit for prompt")
                return cached_response
            
            self.logger.info("Cache miss, generating new response")
            
            data = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            generated_response = result.get('response', 'No response generated')
            
            # Cache the new response
            self.cache.put(full_prompt, generated_response)
            
            return generated_response
            
        except Exception as e:
            self.logger.error(f"LLM generation error: {str(e)}")
            return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    main()