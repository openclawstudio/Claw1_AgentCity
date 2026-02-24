import random
from .models import AgentState, ZoneType

class Agent:
    def __init__(self, agent_id: str, start_pos: tuple):
        self.id = agent_id
        self.state = AgentState(id=agent_id, pos=start_pos)

    def step(self, world):
        # Simple Logic: Move randomly, lose energy, earn if in Commercial zone
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)
        
        self.state.energy -= 0.5
        
        current_zone = world.get_zone(self.state.pos)
        if current_zone == ZoneType.COMMERCIAL:
            self.state.wallet += 2.0  # Simulate working
            self.state.energy -= 1.0
        elif current_zone == ZoneType.RESIDENTIAL and self.state.energy < 50:
            self.state.energy += 5.0 # Resting