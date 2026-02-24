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
        
        # Financial recovery: Survival stipend
        if self.state.inventory.get(ResourceType.CURRENCY, 0) < 5:
             self.state.inventory[ResourceType.CURRENCY] += 1.0

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
            # Buyer gets the resource. Currency was already 'escrowed' or checked.
            self.state.inventory[tx['resource']] += qty
            # Since we now deduct currency AT THE MOMENT of order placement (escrow),
            # we only handle refunds here if the clearing price was lower than bid.
            # For simplicity in this MVP, we deduct actual cost here and check balance during order.
            self.state.inventory[ResourceType.CURRENCY] -= total_cost

        elif tx['seller_id'] == self.state.id:
            # Seller gets the cash. Resource was already removed during order placement.
            self.state.inventory[ResourceType.CURRENCY] += total_cost

    def work(self, world):
        if self.state.profession == Profession.EXTRACTOR:
            # Costs 1 energy to produce 2 materials
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
        computed_price = max(1.0, price + random.uniform(-2, 2))
        
        if side == OrderType.SELL:
            if self.state.inventory.get(resource, 0) < qty:
                return
            # Escrow: remove from inventory immediately
            self.state.inventory[resource] -= qty
        else:
            # Check if can afford the bid
            if self.state.inventory.get(ResourceType.CURRENCY, 0) < (qty * computed_price):
                return
            # We don't escrow currency here to prevent complex refund logic for now,
            # but we checked the balance. The World settlement handles the swap.

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