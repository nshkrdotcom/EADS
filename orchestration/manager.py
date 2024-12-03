"""Agent manager for orchestrating multiple agents."""

from typing import Any, Dict, List, Optional, Type, cast

import ray

from .agent import Agent, AgentConfig


@ray.remote
class AgentManager:
    """Manager for coordinating multiple agents."""

    def __init__(self) -> None:
        """Initialize agent manager."""
        if not ray.is_initialized():
            ray.init()
        self.agents: Dict[str, ray.actor.ActorHandle] = {}

    def add_agent(self, config: AgentConfig, agent_class: Type[Agent] = Agent) -> str:
        """Add a new agent to the system.

        Args:
            config: Agent configuration
            agent_class: Agent class to instantiate

        Returns:
            str: Agent ID
        """
        agent_ref = cast(ray.actor.ActorHandle, ray.remote(agent_class).remote(config))
        self.agents[config.name] = agent_ref
        return config.name

    def remove_agent(self, agent_name: str) -> None:
        """Remove an agent from the system.

        Args:
            agent_name: Name of the agent to remove
        """
        if agent_name in self.agents:
            ray.kill(self.agents[agent_name])
            del self.agents[agent_name]

    async def send_message(
        self, from_agent: str, to_agent: str, content: Dict[str, Any]
    ) -> None:
        """Send a message between agents.

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            content: Message content
        """
        if to_agent in self.agents:
            message = {
                "from": from_agent,
                "content": content,
                "timestamp": ray.get_runtime_context().get_time(),
            }
            await cast(
                ray.actor.ActorHandle, self.agents[to_agent]
            ).receive_message.remote(message)

    async def process_all_messages(self) -> Dict[str, List[Dict[str, Any]]]:
        """Process messages for all agents.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Responses from each agent
        """
        futures = {
            name: cast(ray.actor.ActorHandle, agent).process_messages.remote()
            for name, agent in self.agents.items()
        }

        responses: Dict[str, List[Dict[str, Any]]] = {}
        for name, future in futures.items():
            responses[name] = await ray.get(future)

        return responses

    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get the current state of an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Optional[Dict[str, Any]]: Agent's current state if it exists
        """
        if agent_name in self.agents:
            state = ray.get(cast(ray.actor.ActorHandle, self.agents[agent_name]).state)
            return cast(Dict[str, Any], state)
        return None

    def shutdown(self) -> None:
        """Shutdown all agents and cleanup Ray."""
        for agent_name in list(self.agents.keys()):
            self.remove_agent(agent_name)
        ray.shutdown()
