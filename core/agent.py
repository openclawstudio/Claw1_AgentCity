import uuid
import random
from core.models import AgentState, Position

class Citizen:
    def __init__(self, name: str, x: int, y: int):
        self.id = str(uuid.uuid4())[:8]
        self.state = AgentState(id=self.id, name=name, pos=Position(x=x, y=y))

    def step(self, world):
        # Basic AI logic: Survive and Trade
        self.state.energy -= 0.5
        
        # Decision tree
        if self.state.energy < 30:
            self.seek_energy(world)
        elif self.state.wallet > 20:
            self.seek_commerce(world)
        else:
            self.wander(world)

    def wander(self, world):
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        new_x = max(0, min(world.state.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.state.height - 1, self.state.pos.y + dy))
        self.state.pos.x = new_x
        self.state.pos.y = new_y

    def seek_energy(self, world):
        # In an MVP, residential zones replenish energy for a cost
        if world.get_district_at(self.state.pos.x, self.state.pos.y) == "RESIDENTIAL":
            cost = world.economy.get_market_price("ENERGY")
            if self.state.wallet >= cost:
                self.state.wallet -= cost
                self.state.energy += 20
                world.economy.record_transaction(self.id, "CITY_RENT", cost, "ENERGY", world.state.tick)
        else:
            self.wander(world)

    def seek_commerce(self, world):
        # Commercial zones allow 'working' (gaining wallet, losing energy)
        if world.get_district_at(self.state.pos.x, self.state.pos.y) == "COMMERCIAL":
            self.state.wallet += world.economy.get_market_price("COMMERCE")
            self.state.energy -= 2
        else:
            self.wander(world)