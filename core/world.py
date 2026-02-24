import random
from typing import Dict
from .agent import Citizen
from .economy import EconomySystem

class World:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.agents: Dict[str, Citizen] = {}
        self.businesses = {}
        self.economy = EconomySystem()
        self.tick_counter = 0

    def spawn_agent(self):
        x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
        agent_id = f"agent_{self.tick_counter}_{random.randint(0, 1000)}"
        agent = Citizen(agent_id, x, y)
        self.agents[agent_id] = agent
        return agent

    def create_business(self, owner_id, pos, b_type):
        from .models import BusinessState
        b_id = f"biz_{len(self.businesses)}_{random.randint(0, 1000)}"
        new_biz = BusinessState(id=b_id, owner_id=owner_id, pos=pos, business_type=b_type)
        self.businesses[b_id] = new_biz
        return new_biz

    def tick(self):
        self.tick_counter += 1
        
        # Process agent actions
        for agent_id in list(self.agents.keys()):
            agent = self.agents.get(agent_id)
            if not agent: continue
            
            agent.step(self)
            
            if agent.state.energy <= 0:
                print(f"Agent {agent_id} has perished.")
                del self.agents[agent_id]
        
        # Sustainability: Spawn new citizens if population drops too low
        if len(self.agents) < 5:
            self.spawn_agent()

        if self.tick_counter % 10 == 0:
            total_wealth = sum(a.state.balance for a in self.agents.values())
            print(f"[Tick {self.tick_counter}] Pop: {len(self.agents)} | Biz: {len(self.businesses)} | GDP: {total_wealth:.1f}")