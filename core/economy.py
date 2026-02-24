from typing import Dict, List, Any, Union
from .models import AgentState, BusinessState

class EconomySystem:
    def __init__(self):
        self.total_money_supply = 0.0
        self.transaction_history: List[Dict[str, Any]] = []
        self.job_board = []

    def post_job(self, business_id: str, title: str, wage: float):
        job = {"business_id": business_id, "title": title, "wage": wage, "active": True}
        self.job_board.append(job)
        return job

    def transfer(self, sender: Union[AgentState, BusinessState], receiver: Union[AgentState, BusinessState], amount: float) -> bool:
        """
        Safely transfers funds between agents or businesses.
        Handles both AgentState (balance) and BusinessState (vault).
        """
        if amount <= 0:
            return False

        # Determine sender balance
        s_bal = getattr(sender, "balance", getattr(sender, "vault", 0.0))
        
        if s_bal < amount:
            return False

        # Deduct from sender
        if hasattr(sender, "balance"):
            sender.balance -= amount
        else:
            sender.vault -= amount

        # Add to receiver
        if hasattr(receiver, "balance"):
            receiver.balance += amount
        elif hasattr(receiver, "vault"):
            receiver.vault += amount
        else:
            # Refund if no wallet found
            if hasattr(sender, "balance"): sender.balance += amount
            else: sender.vault += amount
            return False

        self.transaction_history.append({
            "from": getattr(sender, "id", "unknown"), 
            "to": getattr(receiver, "id", "unknown"), 
            "amount": amount
        })
        return True