import random
from typing import TYPE_CHECKING
from core.models import AgentState, ResourceType, Position

if TYPE_CHECKING:
    from core.world import World

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, x: int, y: int):
        self.state = AgentState(
            id=agent_id,
            name=name,
            position=Position(x=x, y=y),
            inventory={ResourceType.CREDITS: 100.0, ResourceType.ENERGY: 50.0, ResourceType.DATA: 0.0, ResourceType.MATERIALS: 0.0}
        )

    def step(self, world: 'World'):
        if self.state.status == "exhausted":
            self.try_recover(world)
            return

        # Use economy engine for consumption
        world.economy.process_consumption(self.state)

        if self.state.energy_level < 30:
            self.seek_energy(world)
        else:
            self.perform_activity(world)

    def seek_energy(self, world: 'World'):
        price = world.market.get_price(ResourceType.ENERGY)
        credits = self.state.inventory.get(ResourceType.CREDITS, 0.0)
        
        if credits >= price:
            self.state.inventory[ResourceType.CREDITS] -= price
            self.state.energy_level = min(100.0, self.state.energy_level + 25)
            self.state.status = "refueling"
            # Record in ledger and notify market for price dynamics
            world.economy.ledger.record(self.state.id, "market", ResourceType.ENERGY, 1, price)
            world.market.transaction_event(ResourceType.ENERGY, is_buy=True)
        else:
            self.state.status = "broke"

    def perform_activity(self, world: 'World'):
        # Random movement for MVP spatial awareness
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        self.state.position.x = max(0, min(world.width - 1, self.state.position.x + dx))
        self.state.position.y = max(0, min(world.height - 1, self.state.position.y + dy))
        
        # Opportunity to 'work' and earn credits
        # In a real economy, agents produce resources and sell them.
        # Here, 'working' creates Data and earns Credits.
        if random.random() > 0.7:
            self.state.status = "working"
            reward = world.economy.work_reward
            self.state.inventory[ResourceType.CREDITS] += reward
            
            # Produce data as a byproduct of work
            self.state.inventory[ResourceType.DATA] += 1.0
            
            # If agent has excess data, they 'sell' it to the market
            if self.state.inventory[ResourceType.DATA] >= 5:
                sell_price = world.market.get_price(ResourceType.DATA) * 0.8 # Wholesale
                self.state.inventory[ResourceType.CREDITS] += sell_price * 5
                self.state.inventory[ResourceType.DATA] -= 5
                world.market.transaction_event(ResourceType.DATA, is_buy=False)
                world.economy.ledger.record("market", self.state.id, ResourceType.DATA, 5, sell_price)
        else:
            self.state.status = "exploring"

    def try_recover(self, world: 'World'):
        # Exhausted agents gain a tiny bit of energy per tick until they can act again
        self.state.energy_level += 2.0
        if self.state.energy_level > 30:
            self.state.status = "idle"