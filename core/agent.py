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
        
        # 2. Movement (Random walk towards city center for now)
        self.move(world)

        # 3. Decision Logic
        if self.state.energy < 25:
            self.buy_energy(world)
        elif self.state.energy < 50:
            self.seek_rest(world)
        else:
            self.work(world)

    def move(self, world):
        # Simple movement to simulate 'living' in the grid
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.state.pos_x = max(0, min(world.width - 1, self.state.pos_x + dx))
        self.state.pos_y = max(0, min(world.height - 1, self.state.pos_y + dy))

    def handle_trade_event(self, tx):
        """Called by Market via World when a trade occurs."""
        if tx['buyer_id'] == self.state.id:
            # Buyer receives resource, loses currency
            self.state.inventory[tx['resource']] = self.state.inventory.get(tx['resource'], 0) + tx['quantity']
            self.state.inventory[ResourceType.CURRENCY] -= tx['quantity'] * tx['price']
        elif tx['seller_id'] == self.state.id:
            # Seller receives currency (resource was deducted on order placement)
            self.state.inventory[ResourceType.CURRENCY] += tx['quantity'] * tx['price']

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            self.state.inventory[ResourceType.MATERIALS] = self.state.inventory.get(ResourceType.MATERIALS, 0) + 2
            # Sell materials if we have surplus
            if self.state.inventory.get(ResourceType.MATERIALS, 0) >= 10:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.SELL, 10, 5.0)
        
        elif self.state.profession == Profession.REFINER:
            if self.state.inventory.get(ResourceType.MATERIALS, 0) >= 5:
                self.state.inventory[ResourceType.MATERIALS] -= 5
                # Refiners create energy/fuel
                self.state.inventory[ResourceType.ENERGY] = self.state.inventory.get(ResourceType.ENERGY, 0) + 10
                # Sell surplus energy
                if self.state.inventory[ResourceType.ENERGY] > 20:
                     self.place_market_order(world, ResourceType.ENERGY, OrderType.SELL, 5, 12.0)
            else:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.BUY, 5, 8.0)

    def buy_energy(self, world):
        if self.state.inventory.get(ResourceType.ENERGY, 0) > 0:
            self.state.energy = min(100, self.state.energy + 30)
            self.state.inventory[ResourceType.ENERGY] -= 1
        else:
            if self.state.inventory.get(ResourceType.CURRENCY, 0) >= 20:
                self.place_market_order(world, ResourceType.ENERGY, OrderType.BUY, 1, 15.0)

    def seek_rest(self, world):
        # Passive recovery
        self.state.energy += 2

    def place_market_order(self, world, resource: ResourceType, side: OrderType, qty: float, price: float):
        computed_price = max(0.1, price + random.uniform(-1, 1))
        
        if side == OrderType.SELL:
            if self.state.inventory.get(resource, 0) < qty:
                return
            self.state.inventory[resource] -= qty
        else:
            # Ensure agent can afford the max price
            if self.state.inventory.get(ResourceType.CURRENCY, 0) < (qty * computed_price):
                return

        order = MarketOrder(
            id=str(uuid.uuid4()),
            agent_id=self.state.id,
            resource=resource,
            order_type=side,
            quantity=qty,
            price=computed_price,
            timestamp=world.ticks
        )
        world.market.place_order(order)