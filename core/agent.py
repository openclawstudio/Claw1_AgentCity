import random
import logging
from .models import Entity, Position

logger = logging.getLogger("Agent")

class Citizen(Entity):
    goal: str = "explore"

    async def update(self, world):
        # Basic AI logic: Random movement for MVP phase
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = max(0, min(world.width - 1, self.position.x + dx))
        new_y = max(0, min(world.height - 1, self.position.y + dy))
        
        self.position = Position(x=new_x, y=new_y)
        self.energy -= 0.1
        
        if self.energy < 20:
            self.goal = "find_food"
        elif self.energy > 80:
            self.goal = "work"