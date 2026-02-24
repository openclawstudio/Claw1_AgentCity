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
            inventory={
                ResourceType.CREDITS: 100.0, 
                ResourceType.ENERGY: 50.0, 
                ResourceType.DATA: 0.0, 
                ResourceType.MATERIALS: 0.0
            }
        )

    def step(self, world: 'World'):
        if self.state.status == "exhausted":
            self.try_recover()
            return

        # Reset status for new tick unless specialized
        if self.state.status not in ["exhausted", "broke"]:
            self.state.status = "idle"

        # 1. Metabolism
        world.economy.process_consumption(self.state)

        # 2. Decision logic
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
            # Record: Agent pays Market for Energy
            world.economy.ledger.record(self.state.id, "market", ResourceType.ENERGY, 1, price)
            world.market.transaction_event(ResourceType.ENERGY, is_buy=True)
        else:
            self.state.status = "broke"

    def perform_activity(self, world: 'World'):
        self.move_randomly(world)
        
        # Economic logic: Work and Trade
        if random.random() > 0.7:
            world.economy.apply_work_effects(self.state)
            
            # Sell surplus data
            if self.state.inventory[ResourceType.DATA] >= 5:
                sell_price = world.market.get_price(ResourceType.DATA) * 0.8
                qty = 5
                self.state.inventory[ResourceType.CREDITS] += (sell_price * qty)
                self.state.inventory[ResourceType.DATA] -= qty
                world.market.transaction_event(ResourceType.DATA, is_buy=False)
                # Record: Agent sells to Market
                world.economy.ledger.record(self.state.id, "market", ResourceType.DATA, qty, sell_price)
        else:
            self.state.status = "exploring"

    def move_randomly(self, world: 'World'):
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        new_x = max(0, min(world.width - 1, self.state.position.x + dx))
        new_y = max(0, min(world.height - 1, self.state.position.y + dy))
        self.state.position = Position(x=new_x, y=new_y)

    def try_recover(self):
        self.state.energy_level += 5.0
        if self.state.energy_level > 30:
            self.state.status = "idle"