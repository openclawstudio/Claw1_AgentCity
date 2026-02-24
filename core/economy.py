from typing import List
from .models import Transaction, ResourceType

class Economy:
    def __init__(self):
        self.transaction_history: List[Transaction] = []
        self.tax_rate = 0.05
        self.treasury = 0.0

    def transfer(self, sender, receiver, amount: float, resource: ResourceType, tick: int) -> bool:
        if sender.balance >= amount:
            tax = amount * self.tax_rate
            net_amount = amount - tax
            
            sender.balance -= amount
            receiver.balance += net_amount
            self.treasury += tax
            
            tx = Transaction(
                sender_id=sender.id, 
                receiver_id=receiver.id, 
                amount=amount, 
                resource_type=resource, 
                timestamp=tick
            )
            self.transaction_history.append(tx)
            return True
        return False