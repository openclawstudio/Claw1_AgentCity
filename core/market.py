import uuid
from typing import List, Dict
from .models import MarketOrder, OrderType, ResourceType

class Market:
    def __init__(self):
        self.order_book: Dict[ResourceType, List[MarketOrder]] = {
            res: [] for res in ResourceType
        }
        self.transaction_history = []

    def place_order(self, order: MarketOrder):
        self.order_book[order.resource].append(order)
        self.match_orders(order.resource)

    def match_orders(self, resource: ResourceType):
        buys = sorted([o for o in self.order_book[resource] if o.order_type == OrderType.BUY], key=lambda x: x.price, reverse=True)
        sells = sorted([o for o in self.order_book[resource] if o.order_type == OrderType.SELL], key=lambda x: x.price)

        while buys and sells and buys[0].price >= sells[0].price:
            buy = buys.pop(0)
            sell = sells.pop(0)
            
            traded_qty = min(buy.quantity, sell.quantity)
            price = sell.price # Seller's price is the clearing price
            
            # Logic for partial fills would go here, omitting for MVP brevity
            self.transaction_history.append({
                "buyer": buy.agent_id,
                "seller": sell.agent_id,
                "resource": resource,
                "quantity": traded_qty,
                "price": price
            })
            
            # Clean up original order book
            self.order_book[resource] = [o for o in self.order_book[resource] if o.id != buy.id and o.id != sell.id]
            
            # Handle leftovers
            if buy.quantity > traded_qty:
                buy.quantity -= traded_qty
                self.order_book[resource].append(buy)
            if sell.quantity > traded_qty:
                sell.quantity -= traded_qty
                self.order_book[resource].append(sell)