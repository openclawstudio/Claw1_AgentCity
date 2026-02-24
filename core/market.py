from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    item: str
    price: float
    order_type: str # 'buy' or 'sell'

class Market:
    def __init__(self):
        self.listings: List[Order] = []

    def post_order(self, order: Order):
        self.listings.append(order)

    def find_match(self, item: str, max_price: float) -> Optional[Order]:
        matches = [o for o in self.listings if o.item == item and o.order_type == 'sell' and o.price <= max_price]
        if not matches:
            return None
        # Return cheapest option
        return min(matches, key=lambda x: x.price)

    def remove_order(self, order_id: str):
        self.listings = [o for o in self.listings if o.id != order_id]