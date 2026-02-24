import random
import uuid
from .models import AgentState, Profession, ResourceType, MarketOrder, OrderType

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        # Initialize inventory with all resource types to avoid KeyErrors
        inventory = {res: 0.0 for res in ResourceType}
        inventory[ResourceType.CURRENCY] = 100.0
        
        self.state = AgentState(
            id=agent_id, 
            pos_x=x, 
            pos_y=y,
            energy=100.0,
            inventory=inventory,
            profession=random.choice([p for p in Profession if p != Profession.UNEMPLOYED])
        )

    def step(self, world):
        # 1. Energy lifecycle
        self.state.energy -= 0.5
        
        # 2. Movement
        self.move(world)

        # 3. Decision Logic
        if self.state.energy < 30:
            self.consume_energy(world)
        
        if self.state.energy < 70:
            self.work(world)
        
        # Financial recovery: Small baseline activity stipend
        if self.state.inventory.get(ResourceType.CURRENCY, 0) < 5:
             self.state.inventory[ResourceType.CURRENCY] += 0.1

    def move(self, world):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.state.pos_x = max(0, min(world.width - 1, self.state.pos_x + dx))
        self.state.pos_y = max(0, min(world.height - 1, self.state.pos_y + dy))

    def handle_trade_event(self, tx):
        """Reconcile balances after trade success."""
        qty = tx['quantity']
        actual_cost = qty * tx['price']

        if tx['buyer_id'] == self.state.id:
            self.state.inventory[tx['resource']] += qty
            # Refund the difference between bid escrow and actual clearing price
            bid_escrow = qty * tx['bid_price']
            refund = bid_escrow - actual_cost
            if refund > 0:
                self.state.inventory[ResourceType.CURRENCY] += refund

        elif tx['seller_id'] == self.state.id:
            self.state.inventory[ResourceType.CURRENCY] += actual_cost

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            self.state.energy -= 1.0
            self.state.inventory[ResourceType.MATERIALS] += 2.0
            if self.state.inventory[ResourceType.MATERIALS] >= 10:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.SELL, 5, 5.0)
        
        elif self.state.profession == Profession.REFINER:
            if self.state.inventory[ResourceType.MATERIALS] >= 5:
                self.state.energy -= 1.0
                self.state.inventory[ResourceType.MATERIALS] -= 5.0
                self.state.inventory[ResourceType.ENERGY] += 8.0
                if self.state.inventory[ResourceType.ENERGY] > 15:
                     self.place_market_order(world, ResourceType.ENERGY, OrderType.SELL, 5, 12.0)
            else:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.BUY, 5, 8.0)

    def consume_energy(self, world):
        if self.state.inventory.get(ResourceType.ENERGY, 0) >= 1:
            self.state.inventory[ResourceType.ENERGY] -= 1
            self.state.energy = min(100.0, self.state.energy + 25.0)
        else:
            self.place_market_order(world, ResourceType.ENERGY, OrderType.BUY, 2, 15.0)

    def place_market_order(self, world, resource: ResourceType, side: OrderType, qty: float, price: float):
        computed_price = max(1.0, price + random.uniform(-1, 1))
        
        if side == OrderType.SELL:
            if self.state.inventory.get(resource, 0) < qty:
                return
            self.state.inventory[resource] -= qty
        else:
            total_bid = qty * computed_price
            if self.state.inventory.get(ResourceType.CURRENCY, 0) < total_bid:
                return
            self.state.inventory[ResourceType.CURRENCY] -= total_bid

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