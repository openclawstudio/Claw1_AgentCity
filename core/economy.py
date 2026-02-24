from typing import List, Dict, Any, Union, Protocol
from .models import AgentState, BusinessState

class Account(Protocol):
    id: str
    balance: float

class EconomySystem:
    def __init__(self):
        self.transaction_history: List[Dict[str, Any]] = []
        self.job_board: List[Dict[str, Any]] = []

    def post_job(self, business_id: str, title: str, wage: float):
        job = {"business_id": business_id, "title": title, "wage": wage, "active": True}
        self.job_board.append(job)
        return job

    def transfer(self, sender: Account, receiver: Account, amount: float) -> bool:
        """
        Safely transfers funds between accounts (Agents or Businesses).
        """
        if amount <= 0 or sender.balance < amount:
            return False

        sender.balance -= amount
        receiver.balance += amount

        self.transaction_history.append({
            "from": sender.id, 
            "to": receiver.id, 
            "amount": amount
        })
        return True