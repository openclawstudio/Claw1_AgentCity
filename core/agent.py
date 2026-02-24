import random
from .models import AgentState, Position

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, start_pos: Position):
        self.state = AgentState(
            id=agent_id,
            name=name,
            pos=start_pos
        )

    def decide_action(self, world_context: dict):
        # Basic survival logic
        if self.state.energy < 30:
            self.state.last_action = "seeking_rest"
            return "move_to_residential"
        
        if self.state.wallet < 10:
            self.state.last_action = "seeking_work"
            return "move_to_industrial"

        self.state.last_action = "wandering"
        return "random_move"

    def move(self, dx: int, dy: int, max_x: int, max_y: int):
        new_x = max(0, min(max_x - 1, self.state.pos.x + dx))
        new_y = max(0, min(max_y - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)