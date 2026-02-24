import uuid
import random
from .market import Market
from .agent import Citizen

class CityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.ticks = 0
        self.market = Market()
        self.agents = {}
        self.market.on_trade_executed.append(self._settle_trade)

    def spawn_agent(self):
        agent_id = f"agent_{self.uuid_id()}"
        agent = Citizen(
            agent_id=agent_id,
            x=random.randint(0, self.width-1),
            y=random.randint(0, self.height-1)
        )
        self.agents[agent_id] = agent

    def _settle_trade(self, tx):
        buyer = self.agents.get(tx['buyer_id'])
        seller = self.agents.get(tx['seller_id'])
        
        # Atomic trade: only update if both parties still exist
        if buyer and seller:
            buyer.handle_trade_event(tx)
            seller.handle_trade_event(tx)

    def tick(self):
        self.ticks += 1
        
        if len(self.agents) < 10:
            self.spawn_agent()

        agent_ids = list(self.agents.keys())
        for a_id in agent_ids:
            if a_id not in self.agents: continue
            agent = self.agents[a_id]
            agent.step(self)
            
            if agent.state.energy <= 0:
                self._cleanup_agent_orders(agent)
                del self.agents[a_id]
        
        return {
            "tick": self.ticks,
            "transactions": len(self.market.transaction_history),
            "population": len(self.agents)
        }

    def _cleanup_agent_orders(self, agent):
        """Remove orders from book and return escrowed items to agent state before disposal."""
        for res in self.market.order_book:
            remaining_orders = []
            for order in self.market.order_book[res]:
                if order.agent_id == agent.state.id:
                    # Return escrowed resources to the dead agent's state (optional/log-only for now)
                    # In a full sim, we might distribute this to the 'world' or heirs.
                    pass
                else:
                    remaining_orders.append(order)
            self.market.order_book[res] = remaining_orders

    @staticmethod
    def uuid_id():
        return str(uuid.uuid4())[:8]