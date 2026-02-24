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

    @staticmethod
    def consume_resource(agent: AgentState, item: str, energy_gain: float) -> bool:
        """Agent consumes an item from inventory to regain energy."""
        if agent.inventory.get(item, 0) >= 1:
            agent.inventory[item] -= 1
            agent.energy = min(100.0, agent.energy + energy_gain)
            return True
        return False