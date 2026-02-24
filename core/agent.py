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
        # 1. Energy lifecycle
        self.state.energy -= 1.0
        
        # 2. Process Market Outcomes (Basic Settlement Simulation)
        # Note: In a full system, the Market would call a callback or transfer funds
        self._settle_trades(world)

        # 3. Decision Logic
        if self.state.energy < 20:
            self.buy_energy(world)
        elif self.state.energy < 50:
            self.seek_rest(world)
        else:
            self.work(world)

    def _settle_trades(self, world):
        """Process transactions from the world history involving this agent."""
        for tx in world.market.transaction_history[-10:]: # Look at recent trades
            if tx['buyer_id'] == self.state.id:
                # Agent bought something
                cost = tx['quantity'] * tx['price']
                self.state.inventory[tx['resource']] = self.state.inventory.get(tx['resource'], 0) + tx['quantity']
                self.state.inventory[ResourceType.CURRENCY] -= cost
            elif tx['seller_id'] == self.state.id:
                # Agent sold something
                revenue = tx['quantity'] * tx['price']
                self.state.inventory[ResourceType.CURRENCY] += revenue
                # Inventory was already 'reserved' or removed during order placement in this MVP

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
            self.place_market_order(world, ResourceType.ENERGY, OrderType.BUY, 1, 15.0)

    def seek_rest(self, world):
        self.state.energy += 5

    def place_market_order(self, world, resource: ResourceType, side: OrderType, qty: float, price: float):
        # Resource validation
        if side == OrderType.SELL:
            available = self.state.inventory.get(resource, 0)
            if available < qty: return
            self.state.inventory[resource] -= qty

        order = MarketOrder(
            id=str(uuid.uuid4()),
            agent_id=self.state.id,
            resource=resource,
            order_type=side,
            quantity=qty,
            price=price + random.uniform(-1, 1),
            timestamp=world.ticks
        )
        world.market.place_order(order)