from .market import Market
from .agent import Citizen
import random

class CityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.ticks = 0
        self.market = Market()
        self.agents = []

    def spawn_agent(self):
        agent = Citizen(
            agent_id=f"agent_{len(self.agents)}",
            x=random.randint(0, self.width-1),
            y=random.randint(0, self.height-1)
        )
        self.agents.append(agent)

    def tick(self):
        self.ticks += 1
        for agent in self.agents:
            agent.step(self)
        
        return {
            "tick": self.ticks,
            "transactions": len(self.market.transaction_history),
            "population": len(self.agents)
        }