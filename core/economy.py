from typing import Dict, List, Any
from .models import InventoryItem

class EconomySystem:
    def __init__(self):
        self.total_money_supply = 0.0
        self.transaction_history: List[Dict[str, Any]] = []
        self.job_board = []

    def post_job(self, business_id: str, title: str, wage: float):
        job = {"business_id": business_id, "title": title, "wage": wage, "active": True}
        self.job_board.append(job)
        return job

    def transfer(self, sender, receiver, amount: float) -> bool:
        """
        Generic transfer between objects with a 'balance' or 'vault' attribute.
        """
        sender_balance = getattr(sender, "balance", getattr(sender, "vault", 0))
        
        if sender_balance >= amount:
            if hasattr(sender, "balance"):
                sender.balance -= amount
            else:
                sender.vault -= amount
                
            if hasattr(receiver, "balance"):
                receiver.balance += amount
            else:
                receiver.vault += amount
                
            self.transaction_history.append({
                "from": getattr(sender, "id", "unknown"), 
                "to": getattr(receiver, "id", "unknown"), 
                "amount": amount
            })
            return True
        return False