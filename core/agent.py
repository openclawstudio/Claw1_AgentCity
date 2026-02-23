import random
import logging
from core.models import AgentState, Vector2D, JobStatus

logger = logging.getLogger("Agent")

class CitizenAgent:
    def __init__(self, state: AgentState):
        self.state = state

    async def decide_action(self, world):
        if self.state.energy <= 0:
            return 

        # 1. Survival: If low energy and has money, 'buy' food/rest if at market
        if self.state.energy < 40 and self.state.economy.balance >= 10:
            await self.handle_survival(world)
        # 2. Rest: If very low energy and no money, go to park
        elif self.state.energy < 30:
            await self.go_rest(world)
        # 3. Economy: If low on money, go to work
        elif self.state.economy.balance < 20:
            await self.handle_economy(world)
        # 4. Social/Exploration
        else:
            self.wander(world)

    async def handle_survival(self, world):
        zone = world.get_zone(self.state.position)
        if zone == "market":
            self.state.economy.balance -= 10
            self.state.energy = min(100.0, self.state.energy + 40)
            logger.debug(f"{self.state.name} bought supplies.")
        else:
            market_center = Vector2D(x=25, y=25)
            self.move_towards(market_center, world)

    async def go_rest(self, world):
        park_center = Vector2D(x=5, y=5)
        self.move_towards(park_center, world)

    def move_towards(self, target: Vector2D, world):
        new_x, new_y = self.state.position.x, self.state.position.y
        if self.state.position.x < target.x: new_x += 1
        elif self.state.position.x > target.x: new_x -= 1
        if self.state.position.y < target.y: new_y += 1
        elif self.state.position.y > target.y: new_y -= 1
        
        self.state.position.x = max(0, min(world.width - 1, new_x))
        self.state.position.y = max(0, min(world.height - 1, new_y))

    def wander(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        target = Vector2D(x=self.state.position.x + dx, y=self.state.position.y + dy)
        self.move_towards(target, world)

    async def handle_economy(self, world):
        zone = world.get_zone(self.state.position)
        if zone == "market":
            if self.state.energy > 15:
                self.state.economy.balance += 15.0
                self.state.energy -= 10.0
        else:
            market_center = Vector2D(x=25, y=25)
            self.move_towards(market_center, world)