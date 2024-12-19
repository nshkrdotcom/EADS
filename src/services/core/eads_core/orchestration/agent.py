"""Agent implementation for EADS."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import ray


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    name: str
    role: str
    capabilities: List[str]
    memory_limit: int = 1000  # MB
    cpu_limit: float = 1.0  # CPU cores


@ray.remote
class Agent:
    """Base agent class for EADS."""

    def __init__(self, config: AgentConfig):
        """Initialize agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.state: Dict[str, Any] = {}
        self.messages: List[Dict] = []

    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update agent's state.

        Args:
            updates: State updates to apply
        """
        self.state.update(updates)

    def receive_message(self, message: Dict) -> None:
        """Receive a message from another agent.

        Args:
            message: Message content and metadata
        """
        self.messages.append(message)

    def process_messages(self) -> List[Dict]:
        """Process received messages and generate responses.

        Returns:
            List[Dict]: List of response messages
        """
        responses = []
        for msg in self.messages:
            # Process message based on agent's role and capabilities
            response = self._handle_message(msg)
            if response:
                responses.append(response)
        self.messages = []  # Clear processed messages
        return responses

    def _handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle a single message based on agent's role.

        Args:
            message: Message to handle

        Returns:
            Optional[Dict]: Response message if any
        """
        # Base implementation - override in specific agent types
        return None
