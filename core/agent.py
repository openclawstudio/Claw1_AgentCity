import random
from .models import AgentState, Role, InventoryItem

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(id=agent_id, pos=(x, y))
        self.perception_radius = 5

    def step(self, world):
        # 1. Update Vitals
        self.state.energy -= 1.0
        
        # 2. Decision Logic
        if self.state.energy < 30:
            self._seek_energy(world)
        elif self.state.role == Role.CITIZEN and self.state.balance > 1000:
            self._become_entrepreneur(world)
        else:
            self._random_move(world)

    def _random_move(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)

    def _seek_energy(self, world):
        # Look for the nearest business providing energy (placeholder logic for finding locations)
        if world.businesses:
            # Move toward first business as a simple heuristic
            target_pos = list(world.businesses.values())[0].pos
            dx = 1 if target_pos[0] > self.state.pos[0] else -1 if target_pos[0] < self.state.pos[0] else 0
            dy = 1 if target_pos[1] > self.state.pos[1] else -1 if target_pos[1] < self.state.pos[1] else 0
            self.state.pos = (self.state.pos[0] + dx, self.state.pos[1] + dy)
            
            # If at a business, 'recharge'
            if self.state.pos == target_pos and self.state.balance >= 10:
                self.state.balance -= 10
                self.state.energy = min(100.0, self.state.energy + 40)
        else:
            self._random_move(world)

    def _become_entrepreneur(self, world):
        self.state.role = Role.ENTREPRENEUR
        world.create_business(self.state.id, self.state.pos, "Energy Hub")
        print(f"Agent {self.state.id} started an Energy Hub at {self.state.pos}!")