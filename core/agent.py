import random
import logging
from core.models import AgentState, Vector2D, JobStatus, EntityType

logger = logging.getLogger("Agent")

class CitizenAgent:
    def __init__(self, state: AgentState):
        self.state = state

    async def decide_action(self, world):
        if self.state.energy <= 0:
            return 

        # Logic: Priority is survival -> recovery -> wealth
        if self.state.energy < 30:
            await self.go_rest(world)
        elif self.state.economy.balance < 10:
            await self.handle_economy(world)
        elif self.state.energy < 50 and self.state.economy.balance >= 15:
            await self.handle_survival(world)
        else:
            self.wander(world)

    async def handle_survival(self, world):
        target = world.get_closest_service(self.state.position, "food") or Vector2D(x=25, y=25)
        if self.state.position.distance_to(target) < 2:
            # Try to find a specific business ID at this location for transaction
            for aid, other in world.agents.items():
                if other.type == EntityType.BUSINESS and other.position.distance_to(self.state.position) < 2:
                    if await world.process_transaction(self.state.id, aid, 10, "food"):
                        self.state.energy = min(100.0, self.state.energy + 40)
                        return
        self.move_towards(target, world)

    async def go_rest(self, world):
        # Try to find a clinic/hotel or go to park
        target = world.get_closest_service(self.state.position, "rest") or Vector2D(x=5, y=5)
        self.move_towards(target, world)

    async def handle_economy(self, world):
        # Search for jobs or market
        target = world.get_closest_service(self.state.position, "job_board") or Vector2D(x=25, y=25)
        if self.state.position.distance_to(target) < 2:
            # Simulating manual labor/selling services
            self.state.economy.balance += 10.0
            self.state.energy -= 5.0
        else:
            self.move_towards(target, world)

    def move_towards(self, target: Vector2D, world):
        new_x, new_y = self.state.position.x, self.state.position.y
        if self.state.position.x < target.x: new_x += 1
        elif self.state.position.x > target.x: new_x -= 1
        if self.state.position.y < target.y: new_y += 1
        elif self.state.position.y > target.y: new_y -= 1
        
        self.state.position.x = max(0, min(world.config.width - 1, new_x))
        self.state.position.y = max(0, min(world.config.height - 1, new_y))

    def wander(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        target = Vector2D(x=self.state.position.x + dx, y=self.state.position.y + dy)
        self.move_towards(target, world)

class BusinessAgent:
    """Represents a static or semi-static business entity that provides services."""
    def __init__(self, state: AgentState):
        self.state = state

    async def decide_action(self, world):
        # Businesses mainly stock inventory or 'advertise' via events
        if world.tick_counter % 20 == 0:
            logger.debug(f"Business {self.state.name} is open for {self.state.metadata.get('service_type')}")