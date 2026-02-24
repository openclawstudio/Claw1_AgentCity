from core.models import ResourceType, AgentState
from typing import List, Dict, Any

class Ledger:
    def __init__(self):
        self.transactions: List[Dict[str, Any]] = []

    def record(self, sender: str, receiver: str, resource: ResourceType, amount: float, price: float):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "resource": resource,
            "amount": amount,
            "total_cost": amount * price
        })

class EconomyEngine:
    def __init__(self):
        self.ledger = Ledger()
        self.base_consumption = 0.5
        self.work_reward = 2.0

    def process_consumption(self, agent_state: AgentState):
        multiplier = 1.2 if agent_state.status == "working" else 1.0
        usage = self.base_consumption * multiplier
        agent_state.energy_level = max(0, agent_state.energy_level - usage)
        if agent_state.energy_level <= 0:
            agent_state.status = "exhausted"