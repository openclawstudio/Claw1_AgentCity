from .market import Market
from .agent import Citizen
import random

class CityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.ticks = 0
        self.market = Market()
        self.agents = {}
        self.market.on_trade_executed.append(self._settle_trade)

    def spawn_agent(self):
        agent_id = f"agent_{uuid_id()}" # Small helper for uniqueness
        agent = Citizen(
            agent_id=agent_id,
            x=random.randint(0, self.width-1),
            y=random.randint(0, self.height-1)
        )
        self.agents[agent_id] = agent

    def _settle_trade(self, tx):
        # Double check existence to prevent errors on dead agents
        buyer = self.agents.get(tx['buyer_id'])
        seller = self.agents.get(tx['seller_id'])
        
        if buyer:
            buyer.handle_trade_event(tx)
        if seller:
            seller.handle_trade_event(tx)

    def tick(self):
        self.ticks += 1
        
        # Maintain population: Immigration logic
        if len(self.agents) < 5:
            self.spawn_agent()

        # Use list of values to avoid concurrent mutation issues
        agent_ids = list(self.agents.keys())
        for a_id in agent_ids:
            if a_id not in self.agents: continue
            agent = self.agents[a_id]
            agent.step(self)
            
            if agent.state.energy <= 0:
                # Refund market orders before death
                self._cleanup_agent_orders(a_id)
                del self.agents[a_id]
        
        return {
            "tick": self.ticks,
            "transactions": len(self.market.transaction_history),
            "population": len(self.agents)
        }

    def _cleanup_agent_orders(self, agent_id):
        for res in self.market.order_book:
            self.market.order_book[res] = [o for o in self.market.order_book[res] if o.agent_id != agent_id]

def uuid_id():
    import uuid
    return str(uuid.uuid4())[:8]