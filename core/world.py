import random
from .agent import Citizen
from .economy import EconomySystem

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

    def tick(self):
        self.tick_counter += 1
        for agent in self.agents.values():
            agent.step(self)
        
        if self.tick_counter % 10 == 0:
            print(f"--- Tick {self.tick_counter} | Agents: {len(self.agents)} | Total Economy: {sum(a.state.balance for a in self.agents.values())} credits ---")