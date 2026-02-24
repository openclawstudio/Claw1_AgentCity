from typing import List, Dict
from .agent import Citizen
from .economy import Economy
from .market import Marketplace
from .models import Position, EntityType

class Business:
    def __init__(self, business_id: str, pos: Position, business_type: str):
        self.id = business_id
        self.pos = pos
        self.business_type = business_type
        self.vault = 0.0

class AgentCityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.tick_count = 0
        self.agents: List[Citizen] = []
        self.businesses: List[Business] = []
        self.economy = Economy()
        self.marketplace = Marketplace()

    def spawn_agent(self, agent_id: str):
        pos = Position(x=random.randint(0, self.width-1), y=random.randint(0, self.height-1)) if 'random' in globals() else Position(x=self.width//2, y=self.height//2)
        agent = Citizen(agent_id, pos)
        self.agents.append(agent)

    def add_business(self, business_id: str, business_type: str, x: int, y: int):
        biz = Business(business_id, Position(x=x, y=y), business_type)
        self.businesses.append(biz)

    def update(self):
        self.tick_count += 1
        for agent in self.agents:
            agent.step(self)

    def get_status(self):
        return {
            "tick": self.tick_count,
            "population": len(self.agents),
            "businesses": len(self.businesses),
            "treasury": self.economy.treasury
        }

import random