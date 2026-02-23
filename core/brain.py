import logging
from typing import Any, Optional

logger = logging.getLogger("Brain")

class BaseBrain:
    """
    Abstract base for agent decision-making. 
    Can be Hardcoded, Rule-based, or LLM-driven.
    """
    def __init__(self, agent: Any):
        self.agent = agent

    async def decide(self, world: Any) -> str:
        raise NotImplementedError("Brains must implement decide()")

class SimpleBrain(BaseBrain):
    async def decide(self, world: Any) -> str:
        if self.agent.energy < 30:
            return "search_food"
        return "explore"