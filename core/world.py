import random
from typing import List, Dict, Optional
from core.models import WorldState, Position, AgentState, District
from core.economy import EconomyManager

class World:
    def __init__(self, width: int = 20, height: int = 20):
        self.state = WorldState(width=width, height=height)
        self.economy = EconomyManager()
        self.agents: Dict[str, 'Citizen'] = {}
        self.district_map: Dict[tuple, str] = {}
        self._setup_districts()

    def _setup_districts(self):
        # Simple Zoning: Residential (Left), Commercial (Right)
        mid_x = self.state.width // 2
        res_tiles = [(x, y) for x in range(mid_x) for y in range(self.state.height)]
        com_tiles = [(x, y) for x in range(mid_x, self.state.width) for y in range(self.state.height)]
        
        res_district = District(type="RESIDENTIAL", area=res_tiles)
        com_district = District(type="COMMERCIAL", area=com_tiles)
        
        self.state.districts = [res_district, com_district]
        
        # Build lookup map for O(1) performance
        for d in self.state.districts:
            for (x, y) in d.area:
                self.district_map[(x, y)] = d.type

    def add_agent(self, agent):
        self.agents[agent.id] = agent
        # Sync the initial state
        self.state.agents.append(agent.state)

    def get_district_at(self, x: int, y: int) -> str:
        return self.district_map.get((x, y), "WILDERNESS")

    def tick(self):
        self.state.tick += 1
        # Trigger agent logic
        for agent in self.agents.values():
            agent.step(self)
        
        # Ensure WorldState stays in sync with actual agent objects
        self.state.agents = [a.state for a in self.agents.values()]
        return self.state