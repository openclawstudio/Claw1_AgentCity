import random
from core.models import AgentState, ResourceType, Position

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, x: int, y: int):
        self.state = AgentState(
            id=agent_id,
            name=name,
            position=Position(x=x, y=y),
            inventory={ResourceType.CREDITS: 100.0, ResourceType.ENERGY: 50.0}
        )

    def step(self, world):
        if self.state.status == "exhausted":
            self.try_recover(world)
            return

        # Use economy engine for consumption
        world.economy.process_consumption(self.state)

        if self.state.energy_level < 30:
            self.seek_energy(world)
        else:
            self.perform_activity(world)

    def seek_energy(self, world):
        price = world.market.get_price(ResourceType.ENERGY)
        credits = self.state.inventory.get(ResourceType.CREDITS, 0)
        
        if credits >= price:
            self.state.inventory[ResourceType.CREDITS] -= price
            self.state.energy_level += 25
            self.state.status = "refueling"
            world.economy.ledger.record(self.state.id, "market", ResourceType.ENERGY, 1, price)
        else:
            self.state.status = "broke/starving"

    def perform_activity(self, world):
        # Random movement for MVP spatial awareness
        self.state.position.x = max(0, min(world.width - 1, self.state.position.x + random.randint(-1, 1)))
        self.state.position.y = max(0, min(world.height - 1, self.state.position.y + random.randint(-1, 1)))
        
        # Opportunity to 'work' and earn credits/materials
        if random.random() > 0.7:
            self.state.status = "working"
            reward = world.economy.work_reward
            self.state.inventory[ResourceType.CREDITS] = self.state.inventory.get(ResourceType.CREDITS, 0) + reward
        else:
            self.state.status = "exploring"

    def try_recover(self, world):
        # Exhausted agents gain a tiny bit of energy per tick until they can act again
        self.state.energy_level += 0.1
        if self.state.energy_level > 5:
            self.state.status = "idle"