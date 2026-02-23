import random
import logging
from typing import Any
from .models import Entity, Position
from .brain import SimpleBrain

logger = logging.getLogger("Agent")

class Citizen(Entity):
    goal: str = "explore"
    # Use a private attribute for the brain to avoid Pydantic serialization issues with complex objects
    _brain: Any = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self._brain:
            self._brain = SimpleBrain(self)

    async def update(self, world):
        # 1. Perception/Decision
        self.goal = await self._brain.decide(world)
        
        # 2. Action execution (Basic Movement)
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = max(0, min(world.width - 1, self.position.x + dx))
        new_y = max(0, min(world.height - 1, self.position.y + dy))
        
        self.position = Position(x=new_x, y=new_y)
        
        # 3. State decay
        self.energy -= 0.2
        if self.energy < 0:
            self.energy = 0
            logger.warning(f"{self.name} is exhausted!")