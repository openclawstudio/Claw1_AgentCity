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
        credits = self.state.inventory.get(ResourceType.CREDITS, 0.0)
        
        if credits >= price:
            self.state.inventory[ResourceType.CREDITS] = credits - price
            self.state.energy_level += 25
            self.state.status = "refueling"
            # Record in ledger and notify market for price dynamics
            world.economy.ledger.record(self.state.id, "market", ResourceType.ENERGY, 1, price)
            world.market.transaction_event(ResourceType.ENERGY, is_buy=True)
        else:
            self.state.status = "broke/starving"

    def perform_activity(self, world):
        # Random movement for MVP spatial awareness
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        self.state.position.x = max(0, min(world.width - 1, self.state.position.x + dx))
        self.state.position.y = max(0, min(world.height - 1, self.state.position.y + dy))
        
        # Opportunity to 'work' and earn credits
        if random.random() > 0.7:
            self.state.status = "working"
            reward = world.economy.work_reward
            self.state.inventory[ResourceType.CREDITS] = self.state.inventory.get(ResourceType.CREDITS, 0.0) + reward
            # Work produces 'data' for the market
            world.market.transaction_event(ResourceType.DATA, is_buy=False)
        else:
            self.state.status = "exploring"

    def try_recover(self, world):
        # Exhausted agents gain a tiny bit of energy per tick until they can act again
        self.state.energy_level += 1.0
        if self.state.energy_level > 20:
            self.state.status = "idle"