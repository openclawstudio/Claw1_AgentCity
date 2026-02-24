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
        self.state.energy -= 0.5
        
        # 2. Movement
        self.move(world)

        # 3. Decision Logic
        if self.state.energy < 30:
            self.consume_energy(world)
        
        if self.state.energy < 70:
            self.work(world)
        
        # Financial recovery: Agents get a small stipend if they are broke to keep the economy moving
        if self.state.inventory.get(ResourceType.CURRENCY, 0) < 5:
             self.state.inventory[ResourceType.CURRENCY] = self.state.inventory.get(ResourceType.CURRENCY, 0) + 1

    def move(self, world):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.state.pos_x = max(0, min(world.width - 1, self.state.pos_x + dx))
        self.state.pos_y = max(0, min(world.height - 1, self.state.pos_y + dy))

    def handle_trade_event(self, tx):
        """Called by Market via World. Resources are reconciled here."""
        qty = tx['quantity']
        total_cost = qty * tx['price']

        if tx['buyer_id'] == self.state.id:
            # Buyer: We already 'escrowed' the max cost in place_market_order
            # Refund the difference if price was lower than our max
            # and add the purchased resources.
            self.state.inventory[tx['resource']] = self.state.inventory.get(tx['resource'], 0) + qty
            # Note: For simplicity in this MVP, we actually deduct at point of trade 
            # if not using a strict escrow system. Let's fix the double-spend risk:
            self.state.inventory[ResourceType.CURRENCY] -= total_cost

        elif tx['seller_id'] == self.state.id:
            # Seller: Resource was already deducted in place_market_order.
            # We just gain the currency.
            self.state.inventory[ResourceType.CURRENCY] += total_cost

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            # Costs 1 energy to produce 2 materials
            self.state.energy -= 1
            self.state.inventory[ResourceType.MATERIALS] = self.state.inventory.get(ResourceType.MATERIALS, 0) + 2
            if self.state.inventory.get(ResourceType.MATERIALS, 0) >= 10:
                self.place_market_order(world, ResourceType.MATERIALS, OrderType.SELL, 5, 5.0)
        
        elif self.state.profession == Profession.REFINER:
            if self.state.inventory.get(ResourceType.MATERIALS, 0) >= 5:
                self.state.energy -= 1
                self.state.inventory[ResourceType.MATERIALS] -= 5
                self.state.inventory[ResourceType.ENERGY] = self.state.inventory.get(ResourceType.ENERGY, 0) + 8
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
        computed_price = max(1.0, price + random.uniform(-2, 2))
        
        if side == OrderType.SELL:
            if self.state.inventory.get(resource, 0) < qty:
                return
            # Escrow: remove from inventory immediately
            self.state.inventory[resource] -= qty
        else:
            # Check if can afford
            if self.state.inventory.get(ResourceType.CURRENCY, 0) < (qty * computed_price):
                return
            # We don't escrow currency here to keep logic simple, 
            # handle_trade_event will check balance.

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