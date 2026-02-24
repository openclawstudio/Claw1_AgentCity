import random
from .models import AgentState, Role

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(id=agent_id, pos=(x, y))
        self.perception_radius = 5

    def step(self, world):
        """Executes one simulation step for the agent."""
        # 1. Update Vitals
        self.state.energy -= 1.0
        
        # 2. Decision Logic
        if self.state.energy < 30:
            self._seek_energy(world)
        elif self.state.role == Role.CITIZEN and self.state.balance > 1000:
            self._become_entrepreneur(world)
        else:
            self._random_move(world)

    def _move_towards(self, world, target_pos):
        tx, ty = target_pos
        cx, cy = self.state.pos
        
        dx = 1 if tx > cx else -1 if tx < cx else 0
        dy = 1 if ty > cy else -1 if ty < cy else 0
        
        new_pos = (
            max(0, min(world.width - 1, cx + dx)),
            max(0, min(world.height - 1, cy + dy))
        )
        self.state.pos = new_pos

    def _random_move(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)

    def _seek_energy(self, world):
        if world.businesses:
            # Find nearest business (Simple Euclidean heuristic)
            target_biz = min(
                world.businesses.values(), 
                key=lambda b: (b.pos[0]-self.state.pos[0])**2 + (b.pos[1]-self.state.pos[1])**2
            )
            
            if self.state.pos == target_biz.pos:
                # Use Economy System for formal transfer
                owner = world.agents.get(target_biz.owner_id)
                cost = 15.0
                energy_gain = 40.0
                
                if self.state.balance >= cost:
                    success = world.economy.transfer(self.state, owner.state if owner else target_biz, cost)
                    if success:
                        self.state.energy = min(100.0, self.state.energy + energy_gain)
                        if not owner: # If owner is gone, money goes to business vault
                            target_biz.vault += cost
            else:
                self._move_towards(world, target_biz.pos)
        else:
            self._random_move(world)

    def _become_entrepreneur(self, world):
        setup_cost = 500.0
        if self.state.balance >= setup_cost:
            self.state.balance -= setup_cost
            self.state.role = Role.ENTREPRENEUR
            # Entrepreneurs also get a small starting inventory of energy to sell
            world.create_business(self.state.id, self.state.pos, "Energy Hub")
            print(f"Agent {self.state.id} founded a business at {self.state.pos}")