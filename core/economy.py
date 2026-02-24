from typing import Dict
from .models import AgentState, ResourceType

class EconomySystem:
    TAX_RATE = 0.05
    
    @staticmethod
    def process_transaction(buyer: AgentState, seller: AgentState, amount: float, item: str):
        if buyer.wallet >= amount:
            buyer.wallet -= amount
            seller.wallet += amount * (1 - EconomySystem.TAX_RATE)
            
            # Update inventory
            buyer.inventory[item] = buyer.inventory.get(item, 0) + 1
            seller.inventory[item] = max(0, seller.inventory.get(item, 0) - 1)
            return True
        return False

    @staticmethod
    def pay_wage(agent: AgentState, amount: float):
        agent.wallet += amount
        agent.energy -= 10.0 # Working costs energy