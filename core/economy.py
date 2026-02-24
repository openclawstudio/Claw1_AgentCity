from typing import Dict, List, Any

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
        Safely transfers funds between agents or businesses.
        Handles both AgentState (balance) and BusinessState (vault).
        """
        # Determine sender balance
        if hasattr(sender, "balance"):
            s_bal = sender.balance
        elif hasattr(sender, "vault"):
            s_bal = sender.vault
        else:
            return False

        if s_bal < amount:
            return False

        # Deduct
        if hasattr(sender, "balance"):
            sender.balance -= amount
        else:
            sender.vault -= amount

        # Add
        if hasattr(receiver, "balance"):
            receiver.balance += amount
        elif hasattr(receiver, "vault"):
            receiver.vault += amount
        else:
            # If receiver has no wallet, refund sender
            if hasattr(sender, "balance"): sender.balance += amount
            else: sender.vault += amount
            return False

        self.transaction_history.append({
            "from": getattr(sender, "id", "unknown"), 
            "to": getattr(receiver, "id", "unknown"), 
            "amount": amount
        })
        return True