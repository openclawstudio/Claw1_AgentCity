from typing import List
from .agent import Citizen
from .economy import Economy
from .market import Marketplace
from .models import Position

class AgentCityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.tick_count = 0
        self.agents: List[Citizen] = []
        self.economy = Economy()
        self.marketplace = Marketplace()

    def spawn_agent(self, agent_id: str):
        pos = Position(x=self.width//2, y=self.height//2)
        agent = Citizen(agent_id, pos)
        self.agents.append(agent)

    def update(self):
        self.tick_count += 1
        for agent in self.agents:
            agent.step(self)

    def get_status(self):
        return {
            "tick": self.tick_count,
            "population": len(self.agents),
            "treasury": self.economy.treasury
        }