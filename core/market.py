from typing import List, Dict
from pydantic import BaseModel

class Order(BaseModel):
    agent_id: str
    item: str
    price: float
    order_type: str # 'buy' or 'sell'

class Market:
    def __init__(self):
        self.listings: List[Order] = []

    def post_order(self, order: Order):
        self.listings.append(order)

    def find_match(self, item: str, max_price: float):
        matches = [o for o in self.listings if o.item == item and o.order_type == 'sell' and o.price <= max_price]
        return sorted(matches, key=lambda x: x.price)[0] if matches else None

    def remove_order(self, order: Order):
        if order in self.listings:
            self.listings.remove(order)