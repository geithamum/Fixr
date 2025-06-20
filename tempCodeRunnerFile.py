import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("WindowsOSAssistant")

@fast.agent(
  instruction="""You are an agent with access to full filesystem search capabilities on the user's computer with Everything Search, as well as the ability to execute commands on the user's computer using mcp-server-commands.
            If the user asks to open a file, search for the file first, use a command to execute it, then tell the user what you did
            If the user asks to open an application, search for either an executable (.exe) or a shortcut (.ink) file, use a command to execute it, then tell the user what you did"""
)
async def main():
  async with fast.run() as agent:
    await agent()

if __name__ == "__main__":
    asyncio.run(main())