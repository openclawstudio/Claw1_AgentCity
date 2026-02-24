import random
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
        # Decrease energy every tick
        self.state.energy -= 1.0
        
        if self.state.energy < 30:
            self._seek_food(world)
        else:
            self._wander(world)

    def _wander(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos.x = new_x
        self.state.pos.y = new_y

    def _seek_food(self, world):
        # Logic: Find a provider and purchase food
        price = world.marketplace.resource_prices.get("food", 10.0)
        if self.balance >= price:
            # In a real simulation, this would be a transfer to a Business entity
            self.balance -= price
            self.state.energy += 40
            # Record tax if applicable via world economy later
            world.economy.treasury += price * world.economy.tax_rate
            print(f"Agent {self.id} bought food. Energy: {self.state.energy:.1f}")