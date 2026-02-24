from typing import Dict, List
from .models import InventoryItem

class EconomySystem:
    def __init__(self):
        self.total_money_supply = 0.0
        self.transaction_history = []
        self.job_board = []

    def post_job(self, business_id: str, title: str, wage: float):
        job = {"business_id": business_id, "title": title, "wage": wage, "active": True}
        self.job_board.append(job)
        return job

    def transfer(self, sender, receiver, amount: float):
        if sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount
            self.transaction_history.append({"from": sender.id, "to": receiver.id, "amount": amount})
            return True
        return False