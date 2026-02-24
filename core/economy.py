from typing import Dict
from .models import AgentState, ResourceType

class EconomySystem:
    TAX_RATE = 0.05
    
    @staticmethod
    def process_transaction(buyer: AgentState, seller: AgentState, amount: float, item: str):
        # Ensure seller has the item and buyer has the funds
        seller_stock = seller.inventory.get(item, 0)
        if buyer.wallet >= amount and seller_stock > 0:
            buyer.wallet -= amount
            seller.wallet += amount * (1 - EconomySystem.TAX_RATE)
            
            # Update inventory
            buyer.inventory[item] = buyer.inventory.get(item, 0) + 1
            seller.inventory[item] = seller_stock - 1
            return True
        return False

    @staticmethod
    def pay_wage(agent: AgentState, amount: float):
        agent.wallet += amount
        # Working costs energy, but don't drop below zero
        agent.energy = max(0.0, agent.energy - 10.0)