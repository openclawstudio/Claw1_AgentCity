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

    def record_payout(self, employer_id: str, employee_id: str, amount: float, title: str):
        """Centralized method to handle job payouts and GDP tracking."""
        self.global_gdp += amount
        return self.ledger.record(employer_id, employee_id, amount, f"Job: {title}")

    def transfer(self, sender_agent, receiver_agent, amount: float, reason: str):
        if sender_agent.balance >= amount:
            sender_agent.balance -= amount
            receiver_agent.balance += amount
            self.global_gdp += amount
            return self.ledger.record(sender_agent.id, receiver_agent.id, amount, reason)
        return None