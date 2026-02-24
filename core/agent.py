import random
import uuid
from .models import AgentState, Profession, ResourceType, MarketOrder, OrderType

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(
            id=agent_id, 
            pos_x=x, 
            pos_y=y,
            profession=random.choice([p for p in Profession if p != Profession.UNEMPLOYED])
        )

    def step(self, world):
        # 1. Energy lifecycle
        self.state.energy -= 1.0
        
        # 2. Decision Logic
        if self.state.energy < 20:
            self.buy_energy(world)
        elif self.state.energy < 50:
            self.seek_rest(world)
        else:
            self.work(world)

    def handle_trade_event(self, tx):
        """Called by Market via World when a trade occurs."""
        if tx['buyer_id'] == self.state.id:
            self.state.inventory[tx['resource']] = self.state.inventory.get(tx['resource'], 0) + tx['quantity']
            self.state.inventory[ResourceType.CURRENCY] -= tx['quantity'] * tx['price']
        elif tx['seller_id'] == self.state.id:
            self.state.inventory[ResourceType.CURRENCY] += tx['quantity'] * tx['price']
            # Inventory was already deducted when placing sell order

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            self.state.inventory[ResourceType.MATERIALS] = self.state.inventory.get(ResourceType.MATERIALS, 0) + 2
            if self.state.inventory[ResourceType.MATERIALS] >= 10:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.SELL, 10, 5.0)
        
        elif self.state.profession == Profession.REFINER:
            if self.state.inventory.get(ResourceType.MATERIALS, 0) >= 5:
                self.state.inventory[ResourceType.MATERIALS] -= 5
                self.state.inventory[ResourceType.ENERGY] = self.state.inventory.get(ResourceType.ENERGY, 0) + 10
            else:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.BUY, 5, 6.0)

    def buy_energy(self, world):
        if self.state.inventory.get(ResourceType.ENERGY, 0) > 0:
            self.state.energy += 20
            self.state.inventory[ResourceType.ENERGY] -= 1
        else:
            # Try to buy energy if we have money
            if self.state.inventory.get(ResourceType.CURRENCY, 0) >= 15:
                self.place_market_order(world, ResourceType.ENERGY, OrderType.BUY, 1, 15.0)

    def seek_rest(self, world):
        self.state.energy += 5

    def place_market_order(self, world, resource: ResourceType, side: OrderType, qty: float, price: float):
        # Validate funds/inventory before placing order
        if side == OrderType.SELL:
            if self.state.inventory.get(resource, 0) < qty:
                return
            self.state.inventory[resource] -= qty
        else:
            if self.state.inventory.get(ResourceType.CURRENCY, 0) < (qty * price):
                return

        order = MarketOrder(
            id=str(uuid.uuid4()),
            agent_id=self.state.id,
            resource=resource,
            order_type=side,
            quantity=qty,
            price=max(0.1, price + random.uniform(-1, 1)),
            timestamp=world.ticks
        )
        world.market.place_order(order)