from typing import List
from core.agent import CitizenAgent
from core.market import Market

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tick = 0
        self.agents: List[CitizenAgent] = []
        self.market = Market()

    def add_agent(self, agent: CitizenAgent):
        self.agents.append(agent)

    def step(self):
        self.tick += 1
        self.market.update_prices()
        for agent in self.agents:
            agent.step(self)

    def get_summary(self):
        avg_energy = sum(a.state.energy_level for a in self.agents) / len(self.agents) if self.agents else 0
        return {
            "tick": self.tick,
            "population": len(self.agents),
            "avg_energy": round(avg_energy, 2),
            "market_prices": self.market.prices
        }
