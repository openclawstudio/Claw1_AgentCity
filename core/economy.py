from typing import List, Dict, Any, Union, Protocol

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

    def transfer(self, sender: Any, receiver: Any, amount: float) -> bool:
        """
        Safely transfers funds between accounts (Agents or Businesses).
        Uses duck typing to ensure both objects have a 'balance' attribute.
        """
        if amount <= 0:
            return False
            
        # Use getattr/setattr or direct access safely
        if not hasattr(sender, 'balance') or not hasattr(receiver, 'balance'):
            return False

        if sender.balance < amount:
            return False

        sender.balance -= amount
        receiver.balance += amount

        self.transaction_history.append({
            "from": getattr(sender, 'id', 'unknown'), 
            "to": getattr(receiver, 'id', 'unknown'), 
            "amount": amount
        })
        return True