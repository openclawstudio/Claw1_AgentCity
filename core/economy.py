from typing import Dict, Optional
from .models import AgentState, ResourceType

class EconomySystem:
    TAX_RATE = 0.05
    
    @staticmethod
    def process_transaction(buyer: AgentState, seller: AgentState, item: str, price: float) -> bool:
        """Executes a trade between two agents."""
        if buyer.wallet < price:
            return False
        
        seller_stock = seller.inventory.get(item, 0)
        if seller_stock <= 0:
            return False
            
        # Exchange currency
        buyer.wallet -= price
        tax = price * EconomySystem.TAX_RATE
        seller.wallet += (price - tax)
        
        # Exchange goods
        seller.inventory[item] = seller_stock - 1
        buyer.inventory[item] = buyer.inventory.get(item, 0) + 1
        
        return True

    @staticmethod
    def pay_wage(agent: AgentState, amount: float):
        """Standardized wage payment for labor."""
        agent.wallet += amount
        # Working costs energy
        agent.energy = max(0.0, agent.energy - 5.0)