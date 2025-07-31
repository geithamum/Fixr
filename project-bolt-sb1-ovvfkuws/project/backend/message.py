import asyncio
import os
import time

from mcp_agent.app import MCPApp
from mcp_agent.config import (
    Settings,
    LoggerSettings,
    MCPSettings,
    MCPServerSettings,
    OpenAISettings,
    AnthropicSettings,
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.llm_selector import ModelPreferences
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

# Settings can either be specified programmatically,
# or loaded from mcp_agent.config.yaml/mcp_agent.secrets.yaml
app = MCPApp(name="fixr")  # settings=settings)


async def process_message(user_input: str):
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context
        
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
            result = await llm.generate_str(
                message=user_input,
            )
            print(result)
            return result


if __name__ == "__main__":
    start = time.time()
    asyncio.get_event_loop().run_until_complete(process_message("Close Discord"))
    end = time.time()
    t = end - start

    print(f"Total run time: {t:.2f}s")
