import random
from .models import AgentState, Role, InventoryItem

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(id=agent_id, pos=(x, y))
        self.perception_radius = 2

    def step(self, world):
        # 1. Update Vitals
        self.state.energy -= 0.5
        
        # 2. Decision Logic
        if self.state.energy < 30:
            self._seek_energy(world)
        elif self.state.role == Role.CITIZEN and self.state.balance > 1000:
            self._become_entrepreneur()
        else:
            self._random_move(world)

    def _random_move(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)

    def _seek_energy(self, world):
        # Logic to find shops or rest areas
        pass

    def _become_entrepreneur(self):
        self.state.role = Role.ENTREPRENEUR
        print(f"Agent {self.state.id} is starting a business!")