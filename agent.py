from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams


import asyncio
app = MCPApp(name="windows_os_assistant")

async def os_assistant():
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        os_agent = Agent(
            name="windows_assistant",
            instruction="""You are an agent with access to full filesystem search capabilities on the user's computer with Everything Search, as well as the ability to execute commands on the user's computer using mcp-server-commands.
            If the user asks to open a file, search for the file first, use a command to execute it, then generate a text response, don't call any more tools.
            If the user asks to open an application, search for either an executable (.exe) or a shortcut (.ink) file, use a command to execute it. Always end the loop after executing the command whether it outputs something or not.
            """,
            server_names=["fetch", "mcp-server-commands", "everything-search"]
        )
        
        async with os_agent:
            llm = await os_agent.attach_llm(OpenAIAugmentedLLM)
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit" or user_input.lower() == "quit":
                    break
                else:
                    try:
                        result = await llm.generate(message=user_input, request_params=RequestParams(use_history=True, parallel_tool_calls=True, ))
                        print(result)
                    except Exception as e:
                        print(f"Error: {e}")
                        
            
            
if __name__ == "__main__":
    import time

    start = time.time()
    asyncio.get_event_loop().run_until_complete(os_assistant())
    end = time.time()
    t = end - start

    print(f"Total run time: {t:.2f}s")