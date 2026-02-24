from typing import List
from core.agent import CitizenAgent
from core.entity import Building, BuildingType
from core.models import Position
from core.economy import EconomySystem

class AgentCityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.agents: List[CitizenAgent] = []
        self.buildings: List[Building] = []
        self.economy = EconomySystem()
        self.tick_counter = 0

    def add_agent(self, agent: CitizenAgent):
        self.agents.append(agent)

    def add_building(self, building: Building):
        # Ensure building is within bounds
        building.pos.x = max(0, min(self.width - 1, building.pos.x))
        building.pos.y = max(0, min(self.height - 1, building.pos.y))
        self.buildings.append(building)

    def step(self):
        self.tick_counter += 1
        for agent in self.agents:
            agent.decide(self.economy, self.buildings, self.width, self.height)

    def get_status(self):
        return {
            "tick": self.tick_counter,
            "population": len(self.agents),
            "economic_activity": len(self.economy.ledger.history)
        }