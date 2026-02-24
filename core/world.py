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
        agent_id = f"agent_{len(self.agents)}"
        agent = Citizen(
            agent_id=agent_id,
            x=random.randint(0, self.width-1),
            y=random.randint(0, self.height-1)
        )
        self.agents[agent_id] = agent

    def _settle_trade(self, tx):
        if tx['buyer_id'] in self.agents:
            self.agents[tx['buyer_id']].handle_trade_event(tx)
        if tx['seller_id'] in self.agents:
            self.agents[tx['seller_id']].handle_trade_event(tx)

    def tick(self):
        self.ticks += 1
        # Use list of values to avoid concurrent mutation issues
        for agent in list(self.agents.values()):
            agent.step(self)
            # Simple death mechanic
            if agent.state.energy <= 0:
                del self.agents[agent.state.id]
        
        return {
            "tick": self.ticks,
            "transactions": len(self.market.transaction_history),
            "population": len(self.agents)
        }