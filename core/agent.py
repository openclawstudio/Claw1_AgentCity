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
        Agents operate based on a hierarchy of needs.
        """
        if self.state.energy <= 0:
            return # Incapacitated

        # 1. Survival Check
        if self.state.energy < 30:
            await self.go_rest(world)
        # 2. Economic Check
        elif self.state.economy.balance < 20:
            await self.handle_economy(world)
        # 3. Social/Exploration
        else:
            self.wander(world.width, world.height)

    async def go_rest(self, world):
        # Navigate to a park zone for recovery
        park_center = Vector2D(x=5, y=5)
        if self.state.position.x == park_center.x and self.state.position.y == park_center.y:
            # Resting is handled by world.tick zone logic
            pass
        else:
            self.move_towards(park_center, world.width, world.height)

    def move_towards(self, target: Vector2D, max_x: int, max_y: int):
        new_x, new_y = self.state.position.x, self.state.position.y
        
        if self.state.position.x < target.x: new_x += 1
        elif self.state.position.x > target.x: new_x -= 1
        
        if self.state.position.y < target.y: new_y += 1
        elif self.state.position.y > target.y: new_y -= 1

        # Bounds validation
        self.state.position.x = max(0, min(max_x - 1, new_x))
        self.state.position.y = max(0, min(max_y - 1, new_y))

    def wander(self, max_x: int, max_y: int):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        self.move_towards(
            Vector2D(x=self.state.position.x + dx, y=self.state.position.y + dy), 
            max_x, 
            max_y
        )

    async def handle_economy(self, world):
        zone = world.get_zone(self.state.position)
        if zone == "market":
            # Simulate working: Costs energy, generates balance via a transaction
            if self.state.energy > 15:
                # In a real economy, this would be a payment from a Business entity
                self.state.economy.balance += 15.0
                self.state.energy -= 10.0
                logger.debug(f"Agent {self.state.id} completed a shift at the market.")
        else:
            # Navigate to market district
            market_center = Vector2D(x=25, y=25)
            self.move_towards(market_center, world.width, world.height)