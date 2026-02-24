import uuid
import random
from typing import Optional
from core.models import AgentState, Position

class Citizen:
    def __init__(self, name: str, x: int, y: int):
        self.id = str(uuid.uuid4())[:8]
        self.state = AgentState(
            id=self.id, 
            name=name,
            pos=Position(x=x, y=y),
            inventory={}
        )

    def _log_event(self, message: str):
        """Keep a short memory of recent events."""
        self.state.memory.append(message)
        if len(self.state.memory) > 5:
            self.state.memory.pop(0)

    def step(self, world):
        """Process one simulation tick for the agent."""
        # 1. Metabolism
        self.state.energy = round(max(0, self.state.energy - 0.5), 2)
        
        # 2. Recovery logic
        if self.state.energy <= 0 or self.state.current_goal == "EXHAUSTED":
            if self.state.energy < 100.0:
                self.recover_exhaustion(world)
                return
            else:
                self.state.current_goal = None

        # 3. Decision Tree
        if self.state.energy < 30:
            self.state.current_goal = "FIND_SHELTER"
            self.seek_energy(world)
        elif self.state.wallet > 200:
            self.state.current_goal = "RELAX"
            self.wander(world)
        else:
            self.state.current_goal = "WORK"
            self.seek_commerce(world)

    def recover_exhaustion(self, world):
        self.state.energy = round(min(100.0, self.state.energy + 10.0), 2)
        self.state.current_goal = "EXHAUSTED"

    def wander(self, world):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        self._move_clamped(world, dx, dy)

    def seek_energy(self, world):
        current_zone = world.get_district_at(self.state.pos.x, self.state.pos.y)
        if current_zone == "RESIDENTIAL":
            price = world.economy.get_market_price("ENERGY")
            if self.state.wallet >= price:
                self.state.wallet = round(self.state.wallet - price, 2)
                self.state.energy = min(100.0, self.state.energy + 50)
                world.economy.record_transaction(self.id, "HOUSING_MGMT", price, "ENERGY", world.state.tick)
                self._log_event(f"Purchased Energy for {price}")
            else:
                self.state.energy = round(min(100.0, self.state.energy + 2.0), 2)
        else:
            # Pathfinding: Residential is usually on the left (x < mid)
            dx = -1 if self.state.pos.x > 2 else random.randint(-1, 1)
            dy = random.randint(-1, 1)
            self._move_clamped(world, dx, dy)

    def seek_commerce(self, world):
        current_zone = world.get_district_at(self.state.pos.x, self.state.pos.y)
        if current_zone == "COMMERCIAL":
            wage = world.economy.get_market_price("COMMERCE")
            self.state.wallet = round(self.state.wallet + wage, 2)
            self.state.energy = round(max(0, self.state.energy - 1.5), 2)
            world.economy.record_transaction("MARKET", self.id, wage, "CREDITS", world.state.tick)
            if random.random() < 0.1: self._log_event(f"Earned {wage} credits")
        else:
            # Pathfinding: Commercial is on the right (x > mid)
            dx = 1 if self.state.pos.x < world.state.width - 3 else random.randint(-1, 1)
            dy = random.randint(-1, 1)
            self._move_clamped(world, dx, dy)

    def _move_clamped(self, world, dx: int, dy: int):
        self.state.pos.x = max(0, min(world.state.width - 1, self.state.pos.x + dx))
        self.state.pos.y = max(0, min(world.state.height - 1, self.state.pos.y + dy))