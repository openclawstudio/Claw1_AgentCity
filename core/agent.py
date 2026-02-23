import random
import logging
from typing import Any, Optional, List
from pydantic import PrivateAttr
from .models import Entity, Position, Resource
from .brain import SimpleBrain

logger = logging.getLogger("Agent")

class Citizen(Entity):
    goal: str = "explore"
    kind: str = "agent"
    _brain: Any = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._brain = SimpleBrain(self)

    async def update(self, world):
        if not self.active:
            return

        # 1. Perception/Decision
        nearby = world.get_nearby_entities(self.position, radius=10)
        self.goal = await self._brain.decide(world, nearby)
        
        # 2. Action execution
        dx, dy = 0, 0
        if self.goal == "search_food":
            # Target the first resource found, or move to center if none found
            resources = [e for e in nearby if isinstance(e, Resource) and not e.depleted]
            if resources:
                target = resources[0].position
            else:
                target = Position(x=world.width // 2, y=world.height // 2)
            
            if self.position.x != target.x:
                dx = 1 if target.x > self.position.x else -1
            if self.position.y != target.y:
                dy = 1 if target.y > self.position.y else -1
        else:
            # Wander
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
        
        new_x = max(0, min(world.width - 1, self.position.x + dx))
        new_y = max(0, min(world.height - 1, self.position.y + dy))
        self.position = Position(x=new_x, y=new_y)
        
        # 3. Consumption/Recovery
        if self.goal == "search_food":
            at_resource = [e for e in world.get_nearby_entities(self.position, radius=0) if isinstance(e, Resource)]
            if at_resource:
                res = at_resource[0]
                gain = min(res.value, 100.0 - self.energy)
                self.energy += gain
                logger.info(f"{self.name} consumed {res.name} at {self.position}. Energy: {self.energy:.1f}")

        # 4. State decay
        decay_rate = 0.5 if self.goal == "search_food" else 0.2
        self.energy -= decay_rate
        
        if self.energy <= 0:
            self.energy = 0
            self.active = False
            logger.warning(f"{self.name} has collapsed from exhaustion.")