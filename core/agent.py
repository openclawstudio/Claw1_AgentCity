import random
from .models import AgentState, Position, ZoneType

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, start_pos: Position):
        self.state = AgentState(
            id=agent_id,
            name=name,
            pos=start_pos
        )

    def decide_action(self, world):
        """Determines next movement and updates internal state metadata."""
        # Basic survival logic
        if self.state.energy < 30:
            self.state.last_action = "seeking_rest"
            return self._move_towards_zone(world, ZoneType.RESIDENTIAL)
        
        if self.state.wallet < 10:
            self.state.last_action = "seeking_work"
            return self._move_towards_zone(world, ZoneType.INDUSTRIAL)

        self.state.last_action = "wandering"
        return self._random_move(world)

    def _move_towards_zone(self, world, zone_type: ZoneType):
        # Simple pathfinding: move towards first matching cell found
        target_pos = None
        for cell in world.grid.values():
            if cell.zone == zone_type:
                target_pos = cell.pos
                break
        
        if target_pos:
            dx = 1 if target_pos.x > self.state.pos.x else -1 if target_pos.x < self.state.pos.x else 0
            dy = 1 if target_pos.y > self.state.pos.y else -1 if target_pos.y < self.state.pos.y else 0
            return dx, dy
        return self._random_move(world)

    def _random_move(self, world):
        return random.choice([(0,1), (0,-1), (1,0), (-1,0)])

    def apply_move(self, dx: int, dy: int, max_x: int, max_y: int):
        """Updates the agent's position within grid boundaries."""
        new_x = max(0, min(max_x - 1, self.state.pos.x + dx))
        new_y = max(0, min(max_y - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)