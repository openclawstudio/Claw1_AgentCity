import random
from core.models import AgentState, Vector2D, JobStatus

class CitizenAgent:
    def __init__(self, state: AgentState):
        self.state = state

    async def decide_action(self, world):
        """Autonomous decision making logic"""
        if self.state.energy < 20:
            # Priority 1: Rest in Park
            park_center = Vector2D(x=5, y=5)
            self.move_towards(park_center) 
        elif self.state.economy.balance < 20:
            # Priority 2: Work/Trade in Market
            await self.handle_economy(world)
        else:
            # Priority 3: Social/Explore
            self.wander(world.width, world.height)

    def move_towards(self, target: Vector2D):
        if self.state.position.x < target.x: self.state.position.x += 1
        elif self.state.position.x > target.x: self.state.position.x -= 1
        
        if self.state.position.y < target.y: self.state.position.y += 1
        elif self.state.position.y > target.y: self.state.position.y -= 1

    def wander(self, max_x: int, max_y: int):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        self.state.position.x = max(0, min(max_x - 1, self.state.position.x + dx))
        self.state.position.y = max(0, min(max_y - 1, self.state.position.y + dy))

    async def handle_economy(self, world):
        zone = world.get_zone(self.state.position)
        if zone == "market":
            # Simple labor simulation: trade energy for balance
            if self.state.energy > 10:
                self.state.economy.balance += 10.0
                self.state.energy -= 10.0
        else:
            # Move toward market center
            market_center = Vector2D(x=25, y=25)
            self.move_towards(market_center)