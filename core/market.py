from typing import Dict, List
from core.models import ResourceType

class Market:
    def __init__(self):
        self.prices = {
            ResourceType.ENERGY: 10.0,
            ResourceType.DATA: 15.0,
            ResourceType.MATERIALS: 20.0
        }
        self.orders = []

    def get_price(self, resource: ResourceType) -> float:
        return self.prices.get(resource, 0.0)

    def post_job(self, agent_id: str, resource: ResourceType, reward: float):
        self.orders.append({"issuer": agent_id, "type": resource, "reward": reward})

    def update_prices(self):
        # Basic volatility
        for res in self.prices:
            self.prices[res] *= 1.01 # Inflation simulation