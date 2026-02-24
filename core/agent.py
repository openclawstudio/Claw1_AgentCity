import random
from core.models import AgentState, Position

class CitizenAgent:
    def __init__(self, id: str, name: str, pos: Position):
        self.state = AgentState(id=id, name=name, pos=pos)
        self.services = []

    def decide(self, economy, buildings):
        # Utility-based decision making
        if self.state.energy < 20:
            self.state.current_goal = "rest"
            return self._seek_building(buildings, "home")
        
        if self.state.wealth < 10:
            self.state.current_goal = "work"
            return self._seek_building(buildings, "office")

        self.state.current_goal = "explore"
        return self._random_move()

    def _seek_building(self, buildings, b_type_name):
        targets = [b for b in buildings if b.type.value == b_type_name]
        if targets:
            target = targets[0]
            self._move_towards(target.pos)
            if self.state.pos.x == target.pos.x and self.state.pos.y == target.pos.y:
                self._perform_activity(b_type_name)

    def _move_towards(self, target_pos: Position):
        if self.state.pos.x < target_pos.x: self.state.pos.x += 1
        elif self.state.pos.x > target_pos.x: self.state.pos.x -= 1
        if self.state.pos.y < target_pos.y: self.state.pos.y += 1
        elif self.state.pos.y > target_pos.y: self.state.pos.y -= 1
        self.state.energy -= 0.5

    def _random_move(self):
        self.state.pos.x += random.choice([-1, 0, 1])
        self.state.pos.y += random.choice([-1, 0, 1])
        self.state.energy -= 0.2

    def _perform_activity(self, activity):
        if activity == "home":
            self.state.energy = min(100, self.state.energy + 10)
        elif activity == "office":
            self.state.wealth += 5
            self.state.energy -= 2