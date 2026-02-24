import random
from core.models import AgentState, Position

class CitizenAgent:
    def __init__(self, id: str, name: str, pos: Position):
        self.state = AgentState(id=id, name=name, pos=pos)
        self.services = []

    def decide(self, economy, buildings, world_width, world_height):
        # Utility-based decision making
        if self.state.energy < 30:
            self.state.current_goal = "rest"
            return self._seek_building(economy, buildings, "home")
        
        if self.state.wealth < 20:
            self.state.current_goal = "work"
            return self._seek_building(economy, buildings, "office")

        if self.state.wealth >= 50 and self.state.energy < 80:
            self.state.current_goal = "shop"
            return self._seek_building(economy, buildings, "market")

        self.state.current_goal = "explore"
        return self._random_move(world_width, world_height)

    def _seek_building(self, economy, buildings, b_type_name):
        targets = [b for b in buildings if b.type.value == b_type_name]
        if not targets:
            self.state.current_goal = "lost"
            return

        # Find nearest building of type
        target = min(targets, key=lambda b: abs(b.pos.x - self.state.pos.x) + abs(b.pos.y - self.state.pos.y))
        
        if self.state.pos.x == target.pos.x and self.state.pos.y == target.pos.y:
            self._perform_activity(economy, target)
        else:
            self._move_towards(target.pos)

    def _move_towards(self, target_pos: Position):
        # Move strictly in one axis per tick for grid realism or allow both for Manhattan
        if self.state.pos.x < target_pos.x: self.state.pos.x += 1
        elif self.state.pos.x > target_pos.x: self.state.pos.x -= 1
        elif self.state.pos.y < target_pos.y: self.state.pos.y += 1
        elif self.state.pos.y > target_pos.y: self.state.pos.y -= 1
        
        self.state.energy = max(0.0, self.state.energy - 0.5)

    def _random_move(self, w, h):
        dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0)])
        new_x = max(0, min(w - 1, self.state.pos.x + dx))
        new_y = max(0, min(h - 1, self.state.pos.y + dy))
        self.state.pos.x = new_x
        self.state.pos.y = new_y
        self.state.energy = max(0.0, self.state.energy - 0.2)

    def _perform_activity(self, economy, building):
        b_type = building.type.value
        if b_type == "home":
            self.state.energy = min(100.0, self.state.energy + 15.0)
        elif b_type == "office":
            income = 10.0
            self.state.wealth += income
            self.state.energy = max(0.0, self.state.energy - 5.0)
            economy.ledger.record("CITY_TREASURY", self.state.id, income, "salary")
        elif b_type == "market":
            cost = 15.0
            if self.state.wealth >= cost:
                self.state.wealth -= cost
                self.state.energy = min(100.0, self.state.energy + 30.0)
                economy.ledger.record(self.state.id, "MARKET_OWNER", cost, "groceries")