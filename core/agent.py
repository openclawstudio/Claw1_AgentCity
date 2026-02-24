import random
from typing import TYPE_CHECKING
from core.models import AgentState, ResourceType, Position, AgentStatus

if TYPE_CHECKING:
    from core.world import World

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, x: int, y: int):
        # Initialize state with full inventory dictionary to prevent KeyErrors
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
        if self.state.status == AgentStatus.EXHAUSTED:
            self.try_recover()
            return

        if self.state.status != AgentStatus.BROKE:
            self.state.status = AgentStatus.IDLE

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
            self.state.status = AgentStatus.REFUELING
            world.economy.ledger.record(self.state.id, "market", ResourceType.ENERGY, 1, price)
            world.market.transaction_event(ResourceType.ENERGY, is_buy=True)
        else:
            self.state.status = AgentStatus.BROKE

    def perform_activity(self, world: 'World'):
        self.move_randomly(world)
        
        if random.random() > 0.5:
            world.economy.apply_work_effects(self.state)
            self.trade_surplus(world)
        else:
            self.state.status = AgentStatus.EXPLORING

    def trade_surplus(self, world: 'World'):
        # Trade both Data and Materials
        for res in [ResourceType.DATA, ResourceType.MATERIALS]:
            qty = self.state.inventory.get(res, 0)
            if qty >= 2.0:
                sell_price = world.market.get_price(res) * 0.95
                self.state.inventory[ResourceType.CREDITS] += (sell_price * qty)
                self.state.inventory[res] = 0.0
                world.market.transaction_event(res, is_buy=False)
                world.economy.ledger.record(self.state.id, "market", res, qty, sell_price)

    def move_randomly(self, world: 'World'):
        dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        new_x = max(0, min(world.width - 1, self.state.position.x + dx))
        new_y = max(0, min(world.height - 1, self.state.position.y + dy))
        self.state.position = Position(x=new_x, y=new_y)

    def try_recover(self):
        self.state.energy_level += 5.0
        if self.state.energy_level > 20:
            self.state.status = AgentStatus.IDLE