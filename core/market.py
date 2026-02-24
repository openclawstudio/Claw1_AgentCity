from typing import Dict, List, Optional
from core.models import ResourceType

class Market:
    def __init__(self):
        self.prices = {
            ResourceType.ENERGY: 10.0,
            ResourceType.DATA: 15.0,
            ResourceType.MATERIALS: 20.0,
            ResourceType.CREDITS: 1.0
        }
        self.demand_buffer: Dict[ResourceType, int] = {res: 0 for res in ResourceType}
        self.supply_buffer: Dict[ResourceType, int] = {res: 0 for res in ResourceType}

    def get_price(self, resource: ResourceType) -> float:
        return self.prices.get(resource, 1.0)

    def transaction_event(self, resource: ResourceType, is_buy: bool):
        if resource == ResourceType.CREDITS:
            return
        if is_buy:
            self.demand_buffer[resource] += 1
        else:
            self.supply_buffer[resource] += 1

    def update_prices(self):
        """Dynamic price adjustment based on supply/demand ratio."""
        for res in ResourceType:
            if res == ResourceType.CREDITS:
                continue
                
            demand = self.demand_buffer.get(res, 0)
            supply = self.supply_buffer.get(res, 0)
            
            # Adjust price based on activity
            if demand > supply:
                self.prices[res] *= 1.05
            elif supply > demand:
                self.prices[res] *= 0.95
            
            # Bound prices to realistic ranges
            self.prices[res] = max(1.0, min(500.0, self.prices[res]))
            
            # Decay buffers to favor recent activity
            self.demand_buffer[res] = 0
            self.supply_buffer[res] = 0