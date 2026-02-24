from typing import List, Dict
import uuid

class Ledger:
    def __init__(self):
        self.transactions: List[Dict] = []

    def record(self, sender: str, receiver: str, amount: float, purpose: str):
        entry = {
            "id": str(uuid.uuid4()),
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "purpose": purpose
        }
        self.transactions.append(entry)
        return entry

class EconomyManager:
    def __init__(self):
        self.ledger = Ledger()
        self.global_gdp = 0.0

    def transfer(self, sender_agent, receiver_agent, amount: float, reason: str):
        if sender_agent.balance >= amount:
            sender_agent.balance -= amount
            receiver_agent.balance += amount
            self.global_gdp += amount
            return self.ledger.record(sender_agent.id, receiver_agent.id, amount, reason)
        return None