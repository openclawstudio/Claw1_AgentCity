import random
from .models import AgentState, Position, ResourceType

class Citizen:
    def __init__(self, agent_id: str, pos: Position):
        self.state = AgentState(id=agent_id, pos=pos)
        self.id = agent_id
        self.balance = self.state.balance

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
        # Dummy logic: if near a business, buy food
        price = world.marketplace.resource_prices["food"]
        if self.balance >= price:
            self.balance -= price
            self.state.energy += 40
            print(f"Agent {self.id} bought food. Energy: {self.state.energy}")