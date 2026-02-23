import random
import logging
from core.models import AgentState, Vector2D, JobStatus

logger = logging.getLogger("Agent")

class CitizenAgent:
    def __init__(self, state: AgentState):
        self.state = state

    async def decide_action(self, world):
        """
        Autonomous decision making logic.
        Agents operate based on a hierarchy of needs:
        1. Survival (Energy)
        2. Economy (Money)
        3. Exploration (Social)
        """
        if self.state.energy <= 0:
            return # Incapacitated

        if self.state.energy < 30:
            await self.go_rest(world)
        elif self.state.economy.balance < 20:
            await self.handle_economy(world)
        else:
            self.wander(world.width, world.height)

    async def go_rest(self, world):
        # Head to the park to regen energy
        park_center = Vector2D(x=5, y=5)
        if self.state.position.x == park_center.x and self.state.position.y == park_center.y:
            # Already at park, world.tick() handles regen
            pass
        else:
            self.move_towards(park_center)

    def move_towards(self, target: Vector2D):
        # Implementation of simple A* approach would be better, but manhattan is fine for grid
        if self.state.position.x < target.x: self.state.position.x += 1
        elif self.state.position.x > target.x: self.state.position.x -= 1
        
        if self.state.position.y < target.y: self.state.position.y += 1
        elif self.state.position.y > target.y: self.state.position.y -= 1

    def wander(self, max_x: int, max_y: int):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        new_x = max(0, min(max_x - 1, self.state.position.x + dx))
        new_y = max(0, min(max_y - 1, self.state.position.y + dy))
        self.state.position.x = new_x
        self.state.position.y = new_y

    async def handle_economy(self, world):
        zone = world.get_zone(self.state.position)
        if zone == "market":
            # Transactional logic: Exchange energy for currency
            if self.state.energy > 15:
                self.state.economy.balance += 15.0
                self.state.energy -= 10.0
                logger.debug(f"Agent {self.state.id} worked at market.")
        else:
            # Navigate to market district
            market_center = Vector2D(x=25, y=25)
            self.move_towards(market_center)