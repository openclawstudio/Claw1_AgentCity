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
        agent_id = f"agent_{len(self.agents)}_{random.randint(0, 1000)}"
        agent = Citizen(agent_id, x, y)
        self.agents[agent_id] = agent
        return agent

    def create_business(self, owner_id, pos, b_type):
        b_id = f"biz_{len(self.businesses)}_{random.randint(0, 1000)}"
        new_biz = BusinessState(id=b_id, owner_id=owner_id, pos=pos, business_type=b_type)
        self.businesses[b_id] = new_biz
        return new_biz

    def tick(self):
        self.tick_counter += 1
        dead_agents = []
        
        # Process agent actions
        agent_keys = list(self.agents.keys())
        for agent_id in agent_keys:
            agent = self.agents.get(agent_id)
            if not agent: continue
            
            agent.step(self)
            if agent.state.energy <= 0:
                dead_agents.append(agent_id)
        
        # Cleanup
        for agent_id in dead_agents:
            print(f"Agent {agent_id} has perished from exhaustion.")
            if agent_id in self.agents:
                del self.agents[agent_id]
        
        # Status Update
        if self.tick_counter % 10 == 0:
            total_wealth = sum(a.state.balance for a in self.agents.values())
            print(f"[Tick {self.tick_counter}] Population: {len(self.agents)} | Businesses: {len(self.businesses)} | Civ Wealth: {total_wealth:.2f}")