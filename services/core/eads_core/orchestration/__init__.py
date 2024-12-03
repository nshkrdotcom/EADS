"""Orchestration module for EADS."""

from .agent import Agent, AgentConfig
from .manager import AgentManager

__all__ = ["Agent", "AgentConfig", "AgentManager"]
