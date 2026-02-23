import random
import logging
from typing import Any, Optional
from pydantic import PrivateAttr
from .models import Entity, Position
from .brain import SimpleBrain

logger = logging.getLogger("Agent")

class Citizen(Entity):
    goal: str = "explore"
    _brain: Any = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._brain = SimpleBrain(self)

    async def update(self, world):
        if not self.active:
            return

        # 1. Perception/Decision
        self.goal = await self._brain.decide(world)
        
        # 2. Action execution
        target_pos = self.position
        if self.goal == "search_food":
            # Move toward center (placeholder for food source logic)
            dx = 1 if world.width // 2 > self.position.x else -1
            dy = 1 if world.height // 2 > self.position.y else -1
        else:
            # Wander
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
        
        new_x = max(0, min(world.width - 1, self.position.x + dx))
        new_y = max(0, min(world.height - 1, self.position.y + dy))
        self.position = Position(x=new_x, y=new_y)
        
        # 3. Consumption/Recovery
        if self.goal == "search_food" and self.position.x == world.width // 2 and self.position.y == world.height // 2:
            self.energy = min(100.0, self.energy + 20)
            logger.info(f"{self.name} found food and recovered energy.")

        # 4. State decay
        decay_rate = 0.5 if self.goal == "search_food" else 0.2
        self.energy -= decay_rate
        
        if self.energy <= 0:
            self.energy = 0
            self.active = False
            logger.warning(f"{self.name} has collapsed from exhaustion.")