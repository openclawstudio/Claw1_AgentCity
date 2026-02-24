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
        price = world.marketplace.resource_prices.get("food", 10.0)
        # Seek business
        provider = next((b for b in world.businesses if b.business_type == "grocery"), None)
        
        if provider:
            if world.economy.transfer(self, provider, price, ResourceType.FOOD, world.tick_count):
                self.state.energy += 40
                print(f"Agent {self.id} bought food from {provider.id}. Energy: {self.state.energy:.1f}")
        elif self.balance >= price:
            # Public vendor (fallback)
            self.balance -= price
            world.economy.treasury += price # No net loss to system, behaves as universal store
            self.state.energy += 40