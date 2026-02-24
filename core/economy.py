from typing import List
from .models import Transaction

class EconomyManager:
    def __init__(self):
        self.ledger: List[Transaction] = []

    def transfer(self, sender, receiver, amount: float, purpose: str, tick: int) -> bool:
        if sender.state.wallet >= amount:
            sender.state.wallet -= amount
            receiver.state.wallet += amount
            tx = Transaction(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=amount,
                purpose=purpose,
                timestamp=tick
            )
            self.ledger.append(tx)
            return True
        return False

    def get_total_wealth(self, agents) -> float:
        return sum(a.state.wallet for a in agents)