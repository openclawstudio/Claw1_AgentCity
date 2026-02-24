from typing import Dict, List, Optional
from core.models import ResourceType

class Market:
    def __init__(self):
        self.prices = {
            ResourceType.ENERGY: 10.0,
            ResourceType.DATA: 15.0,
            ResourceType.MATERIALS: 20.0
        }
        self.demand_buffer: Dict[ResourceType, int] = {res: 0 for res in ResourceType}
        self.supply_buffer: Dict[ResourceType, int] = {res: 0 for res in ResourceType}
        self.orders = []

    def get_price(self, resource: ResourceType) -> float:
        return self.prices.get(resource, 0.0)

    def transaction_event(self, resource: ResourceType, is_buy: bool):
        """Track activity to adjust prices based on supply/demand."""
        if is_buy:
            self.demand_buffer[resource] += 1
        else:
            self.supply_buffer[resource] += 1

    def update_prices(self):
        """Dynamic price adjustment based on simple supply/demand ratio."""
        for res in self.prices:
            demand = self.demand_buffer[res]
            supply = self.supply_buffer[res]
            
            # Adjustment factor: more demand -> higher price, more supply -> lower price
            multiplier = 1.0
            if demand > supply:
                multiplier = 1.05
            elif supply > demand:
                multiplier = 0.95
            
            self.prices[res] = max(1.0, self.prices[res] * multiplier)
            
            # Decay buffers
            self.demand_buffer[res] = 0
            self.supply_buffer[res] = 0

    def post_job(self, agent_id: str, resource: ResourceType, reward: float):
        self.orders.append({"issuer": agent_id, "type": resource, "reward": reward})