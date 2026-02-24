import random
import math
from .models import AgentState, Position, ResourceType

class Citizen:
    def __init__(self, agent_id: str, pos: Position):
        self.state = AgentState(id=agent_id, pos=pos)
        self.id = agent_id

    @property
    def balance(self):
        return self.state.balance

    @balance.setter
    def balance(self, value):
        self.state.balance = value

    def step(self, world):
        """Advance the agent's state by one tick."""
        if self.state.energy <= 0:
            return

        self.state.energy -= 0.5
        
        # Priority 1: Survival (Food)
        if self.state.energy < 40:
            self._seek_resource(world, "food")
        # Priority 2: Work (Money)
        elif self.state.balance < 20:
            self._work(world)
        # Priority 3: Idle
        else:
            self._wander(world)

    def _get_distance(self, pos1: Position, pos2: Position) -> float:
        return math.sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)

    def _wander(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos.x = new_x
        self.state.pos.y = new_y

    def _seek_resource(self, world, resource_type: str):
        targets = [b for b in world.businesses if b.business_type == "grocery"]
        if not targets:
            # Emergency fallback: buy from air at high cost if no businesses exist
            if self.balance >= 15:
                self.balance -= 15
                self.state.energy += 30
            return

        # Find nearest business
        nearest = min(targets, key=lambda b: self._get_distance(self.state.pos, b.pos))
        
        if self._get_distance(self.state.pos, nearest.pos) <= 1.0:
            price = world.marketplace.resource_prices.get(resource_type, 10.0)
            if world.economy.transfer(self, nearest, price, ResourceType.FOOD, world.tick_count):
                self.state.energy += 50
        else:
            self._move_towards(nearest.pos)

    def _work(self, world):
        # Simple labor logic: agents can work at any business to earn credits
        if world.businesses:
            target = world.businesses[0]
            if self._get_distance(self.state.pos, target.pos) <= 1.0:
                # Generate value for the city
                wage = 10.0
                world.economy.transfer(target, self, wage, ResourceType.CREDITS, world.tick_count)
                self.state.energy -= 5
            else:
                self._move_towards(target.pos)

    def _move_towards(self, target_pos: Position):
        if self.state.pos.x < target_pos.x: self.state.pos.x += 1
        elif self.state.pos.x > target_pos.x: self.state.pos.x -= 1
        elif self.state.pos.y < target_pos.y: self.state.pos.y += 1
        elif self.state.pos.y > target_pos.y: self.state.pos.y -= 1