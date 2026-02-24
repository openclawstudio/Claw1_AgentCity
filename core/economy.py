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

    def get_total_volume(self) -> float:
        return sum(t["total_cost"] for t in self.transactions)

class EconomyEngine:
    def __init__(self):
        self.ledger = Ledger()
        self.base_consumption = 0.5
        self.work_reward_credits = 2.0
        self.work_reward_data = 0.5

    def process_consumption(self, agent_state: AgentState):
        multiplier = 1.2 if agent_state.status == "working" else 1.0
        usage = self.base_consumption * multiplier
        agent_state.energy_level = max(0.0, agent_state.energy_level - usage)
        if agent_state.energy_level <= 0:
            agent_state.status = "exhausted"

    def apply_work_effects(self, agent_state: AgentState):
        """Standardizes how agents are rewarded for general city labor."""
        agent_state.inventory[ResourceType.CREDITS] += self.work_reward_credits
        agent_state.inventory[ResourceType.DATA] += self.work_reward_data
        agent_state.status = "working"