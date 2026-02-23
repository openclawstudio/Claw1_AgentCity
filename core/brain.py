import logging
from typing import Any, List

logger = logging.getLogger("Brain")

class BaseBrain:
    def __init__(self, agent: Any):
        self.agent = agent

    async def decide(self, world: Any, nearby_entities: List[Any]) -> str:
        raise NotImplementedError("Brains must implement decide()")

class SimpleBrain(BaseBrain):
    async def decide(self, world: Any, nearby_entities: List[Any]) -> str:
        # Check if hungry
        if self.agent.energy < 40:
            return "search_food"
        
        # Logic to potentially interact with businesses (future phase)
        return "explore"