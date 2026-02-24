import uuid
from typing import List, Dict, Callable
from .models import MarketOrder, OrderType, ResourceType

class Market:
    def __init__(self):
        self.order_book: Dict[ResourceType, List[MarketOrder]] = {
            res: [] for res in ResourceType
        }
        self.transaction_history = []
        self.on_trade_executed: List[Callable] = []

    def place_order(self, order: MarketOrder):
        self.order_book[order.resource].append(order)
        self.match_orders(order.resource)

    def match_orders(self, resource: ResourceType):
        buys = sorted([o for o in self.order_book[resource] if o.order_type == OrderType.BUY], key=lambda x: x.price, reverse=True)
        sells = sorted([o for o in self.order_book[resource] if o.order_type == OrderType.SELL], key=lambda x: x.price)

        for buy in buys:
            for sell in sells:
                if buy.quantity <= 0 or sell.quantity <= 0 or buy.agent_id == sell.agent_id:
                    continue
                
                if buy.price >= sell.price:
                    traded_qty = min(buy.quantity, sell.quantity)
                    clearing_price = sell.price

                    trade_record = {
                        "buyer_id": buy.agent_id,
                        "seller_id": sell.agent_id,
                        "resource": resource,
                        "quantity": traded_qty,
                        "price": clearing_price
                    }
                    
                    # Execute callbacks
                    for callback in self.on_trade_executed:
                        callback(trade_record)

                    self.transaction_history.append(trade_record)
                    buy.quantity -= traded_qty
                    sell.quantity -= traded_qty

        # Cleanup book
        self.order_book[resource] = [
            o for o in self.order_book[resource] if o.quantity > 0
        ]
        
        if len(self.transaction_history) > 1000:
            self.transaction_history = self.transaction_history[-500:]