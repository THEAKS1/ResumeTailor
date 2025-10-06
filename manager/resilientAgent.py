"""
resilientAgent.py

Defines a wrapper for ADK agents to add retry logic for resilience.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from utils.retryDecorator import retry_on_server_error

class ResilientAgentTool(AgentTool):
    """
    A custom tool that wraps an ADK Agent to make it resilient.
    The retry logic is now handled by the decorator.
    """
    def __init__(self, agent: Agent):
        super().__init__(
            agent=agent
        )
        self._agent = agent

    @retry_on_server_error
    async def _run(self, **kwargs) -> dict | str:
        """
        Executes the agent's chat method. The retry logic is now handled by the decorator.
        """
        # Build prompt from kwargs and run agent
        prompt = "\n".join(f"{key}: {value}" for key, value in kwargs.items())
        return await self._agent.chat(prompt)
