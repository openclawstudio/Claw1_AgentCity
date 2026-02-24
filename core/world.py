import random
from typing import List
from .agent import Citizen

from .entity import Business
from .economy import Economy
from .market import Marketplace
from .models import Position, Job

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
        pos = Position(x=random.randint(0, self.width-1), y=random.randint(0, self.height-1))
        agent = Citizen(agent_id, pos)
        self.agents.append(agent)

    def add_business(self, business_id: str, business_type: str, x: int, y: int):
        biz = Business(business_id, Position(x=x, y=y), business_type)
        biz.balance = 500.0
        self.businesses.append(biz)

    def update(self):
        self.tick_count += 1
        
        # Businesses post jobs if board is empty
        if not self.marketplace.get_available_jobs() and self.businesses:
            for biz in self.businesses:
                job = Job(
                    job_id=f"job_{self.tick_count}_{biz.id}",
                    employer_id=biz.id,
                    title="Maintenance",
                    salary=15.0,
                    requirements={}
                )
                self.marketplace.post_job(job)

        # Remove dead agents
        self.agents = [a for a in self.agents if a.state.energy > 0]
        
        for agent in self.agents:
            agent.step(self)

    def get_status(self):
        return {
            "tick": self.tick_count,
            "population": len(self.agents),
            "businesses": len(self.businesses),
            "treasury": self.economy.treasury
        }