import random
import uuid
from .models import AgentState, Profession, ResourceType, MarketOrder, OrderType

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(
            id=agent_id, 
            pos_x=x, 
            pos_y=y,
            profession=random.choice(list(Profession))
        )

    def step(self, world):
        # 1. Consume Energy
        self.state.energy -= 1.0
        
        # 2. Decision Logic
        if self.state.energy < 30:
            self.seek_energy(world)
        else:
            self.work(world)

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            # Gather Materials
            self.state.inventory[ResourceType.MATERIALS] = self.state.inventory.get(ResourceType.MATERIALS, 0) + 1
            if self.state.inventory[ResourceType.MATERIALS] >= 5:
                self.sell_goods(world, ResourceType.MATERIALS)
        
    def sell_goods(self, world, resource: ResourceType):
        qty = self.state.inventory.get(resource, 0)
        if qty > 0:
            order = MarketOrder(
                id=str(uuid.uuid4()),
                agent_id=self.state.id,
                resource=resource,
                order_type=OrderType.SELL,
                quantity=qty,
                price=10.0 + random.uniform(-1, 1),
                timestamp=world.ticks
            )
            world.market.place_order(order)
            self.state.inventory[resource] = 0

    def seek_energy(self, world):
        # Simplified: teleport to random store
        self.state.pos_x = random.randint(0, world.width - 1)
        self.state.pos_y = random.randint(0, world.height - 1)
        self.state.energy += 10