import random
from .models import AgentState, Role

class Citizen:
    def __init__(self, agent_id: str, x: int, y: int):
        self.state = AgentState(id=agent_id, pos=(x, y))
        self.perception_radius = 5

    def step(self, world):
        """Executes one simulation step for the agent."""
        if self.state.energy <= 0:
            return

        # 1. Update Vitals (Survival cost)
        self.state.energy -= 0.8
        
        # 2. Decision Logic
        if self.state.energy < 40:
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
        choices = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
        dx, dy = random.choice(choices)
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)

    def _seek_energy(self, world):
        if not world.businesses:
            self._random_move(world)
            return

        # Find nearest business
        target_biz = min(
            world.businesses.values(), 
            key=lambda b: (b.pos[0]-self.state.pos[0])**2 + (b.pos[1]-self.state.pos[1])**2
        )
        
        if self.state.pos == target_biz.pos:
            # Free energy if you own the business
            if target_biz.owner_id == self.state.id:
                self.state.energy = min(100.0, self.state.energy + 50.0)
                return

            owner = world.agents.get(target_biz.owner_id)
            cost = 20.0
            energy_gain = 50.0
            
            # Target the owner's state or the business vault
            receiver = owner.state if owner else target_biz
            if self.state.balance >= cost:
                success = world.economy.transfer(self.state, receiver, cost)
                if success:
                    self.state.energy = min(100.0, self.state.energy + energy_gain)
            else:
                # Can't afford energy, wander in despair
                self._random_move(world)
        else:
            self._move_towards(world, target_biz.pos)

    def _become_entrepreneur(self, world):
        setup_cost = 600.0
        if self.state.balance >= setup_cost:
            self.state.balance -= setup_cost
            self.state.role = Role.ENTREPRENEUR
            biz = world.create_business(self.state.id, self.state.pos, "Energy Hub")
            print(f">>> Agent {self.state.id} founded {biz.id} at {self.state.pos}")