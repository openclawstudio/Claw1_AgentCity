from typing import Dict, List
from pydantic import BaseModel

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    commodity: str = "CREDITS"
    timestamp: int

class EconomyManager:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.prices: Dict[str, float] = {"SHELTER": 10.0, "ENERGY": 5.0, "COMMERCE": 2.0}

    def record_transaction(self, sender_id: str, receiver_id: str, amount: float, commodity: str, tick: int):
        tx = Transaction(sender_id=sender_id, receiver_id=receiver_id, amount=amount, commodity=commodity, timestamp=tick)
        self.transactions.append(tx)
        return tx

    def get_market_price(self, commodity: str) -> float:
        return self.prices.get(commodity, 1.0)