from core.models import ResourceType

class Ledger:
    def __init__(self):
        self.transactions = []

    def record(self, sender: str, receiver: str, resource: ResourceType, amount: float):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "resource": resource,
            "amount": amount
        })

class EconomyEngine:
    def __init__(self):
        self.base_consumption = 0.5
        self.work_reward = 2.0

    def calculate_consumption(self, agent_state):
        return self.base_consumption * (1.2 if agent_state.status == "working" else 1.0)
