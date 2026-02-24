import random
from typing import List, Dict
from core.models import WorldState, Position, AgentState, District
from core.economy import EconomyManager

class World:
    def __init__(self, width: int = 20, height: int = 20):
        self.state = WorldState(width=width, height=height)
        self.economy = EconomyManager()
        self.agents: Dict[str, 'Citizen'] = {}
        self._setup_districts()

    def _setup_districts(self):
        # Simple Zoning
        mid_x = self.state.width // 2
        self.state.districts.append(District(type="RESIDENTIAL", area=[(x, y) for x in range(mid_x) for y in range(self.state.height)]))
        self.state.districts.append(District(type="COMMERCIAL", area=[(x, y) for x in range(mid_x, self.state.width) for y in range(self.state.height)]))

    def add_agent(self, agent):
        self.agents[agent.id] = agent
        self.state.agents.append(agent.state)

    def get_district_at(self, x, y) -> str:
        for d in self.state.districts:
            if (x, y) in d.area:
                return d.type
        return "WILDERNESS"

    def tick(self):
        self.state.tick += 1
        for agent_id, agent in self.agents.items():
            agent.step(self)
        return self.state