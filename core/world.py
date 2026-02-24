import random
from .agent import Citizen
from .economy import EconomySystem
from .models import BusinessState

class World:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.agents = {}
        self.businesses = {}
        self.economy = EconomySystem()
        self.tick_counter = 0

    def spawn_agent(self):
        x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
        agent_id = f"agent_{len(self.agents)}"
        agent = Citizen(agent_id, x, y)
        self.agents[agent_id] = agent
        return agent

    def create_business(self, owner_id, pos, b_type):
        b_id = f"biz_{len(self.businesses)}"
        new_biz = BusinessState(id=b_id, owner_id=owner_id, pos=pos, business_type=b_type)
        self.businesses[b_id] = new_biz
        return new_biz

    def tick(self):
        self.tick_counter += 1
        dead_agents = []
        
        for agent_id, agent in self.agents.items():
            agent.step(self)
            if agent.state.energy <= 0:
                dead_agents.append(agent_id)
        
        for agent_id in dead_agents:
            print(f"Agent {agent_id} has perished.")
            del self.agents[agent_id]
        
        if self.tick_counter % 10 == 0:
            print(f"--- Tick {self.tick_counter} | Agents: {len(self.agents)} | Businesses: {len(self.businesses)} | Total Wealth: {sum(a.state.balance for a in self.agents.values()):.2f} ---")