import uuid
import random
from core.models import AgentState, Position

class Citizen:
    def __init__(self, name: str, x: int, y: int):
        self.id = str(uuid.uuid4())[:8]
        self.state = AgentState(id=self.id, name=name, pos=Position(x=x, y=y))

    def step(self, world):
        # 1. Metabolism
        self.state.energy = round(max(0, self.state.energy - 0.5), 2)
        
        if self.state.energy <= 0:
            self.recover_exhaustion(world)
            return

        # 2. Decision Logic
        if self.state.energy < 30:
            self.state.current_goal = "FIND_SHELTER"
            self.seek_energy(world)
        elif self.state.wallet > 150:
            self.state.current_goal = "RELAX"
            self.wander(world)
        else:
            self.state.current_goal = "WORK"
            self.seek_commerce(world)

    def recover_exhaustion(self, world):
        self.state.energy = round(min(100.0, self.state.energy + 2.0), 2)
        self.state.current_goal = "EXHAUSTED"

    def wander(self, world):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self._move_clamped(world, dx, dy)

    def seek_energy(self, world):
        current_zone = world.get_district_at(self.state.pos.x, self.state.pos.y)
        if current_zone == "RESIDENTIAL":
            cost = world.economy.get_market_price("ENERGY")
            if self.state.wallet >= cost:
                self.state.wallet -= cost
                self.state.energy = min(100.0, self.state.energy + 40)
                world.economy.record_transaction(self.id, "HOUSING_CORP", cost, "ENERGY", world.state.tick)
        else:
            # Move Left towards Residential
            dx = -1 if self.state.pos.x > 0 else 0
            dy = random.choice([-1, 0, 1])
            self._move_clamped(world, dx, dy)

    def seek_commerce(self, world):
        current_zone = world.get_district_at(self.state.pos.x, self.state.pos.y)
        if current_zone == "COMMERCIAL":
            wage = world.economy.get_market_price("COMMERCE")
            self.state.wallet += wage
            self.state.energy -= 1.0
            world.economy.record_transaction("MARKET", self.id, wage, "CREDITS", world.state.tick)
        else:
            # Move Right towards Commercial
            dx = 1 if self.state.pos.x < world.state.width - 1 else 0
            dy = random.choice([-1, 0, 1])
            self._move_clamped(world, dx, dy)

    def _move_clamped(self, world, dx, dy):
        new_x = max(0, min(world.state.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.state.height - 1, self.state.pos.y + dy))
        self.state.pos.x = new_x
        self.state.pos.y = new_y
