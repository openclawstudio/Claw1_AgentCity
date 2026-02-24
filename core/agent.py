import random
from typing import List, Optional
from core.models import AgentState, Position
from core.entity import Building

class CitizenAgent:
    """An autonomous AI agent with needs, goals, and economic capacity."""
    def __init__(self, id: str, name: str, pos: Position):
        self.state = AgentState(id=id, name=name, pos=pos)

    def decide(self, economy, buildings: List[Building], world_width: int, world_height: int):
        """Main decision logic based on internal utility."""
        # 1. Update Current Building Status (Exit if moving elsewhere)
        
        # 2. Determine Goal based on state
        if self.state.energy < 20:
            self.state.current_goal = "rest"
            return self._seek_building(economy, buildings, "home")
        
        if self.state.wealth < 10:
            self.state.current_goal = "work"
            return self._seek_building(economy, buildings, "office")

        if self.state.wealth >= 30 and self.state.energy < 70:
            self.state.current_goal = "shop"
            return self._seek_building(economy, buildings, "market")

        self.state.current_goal = "explore"
        return self._random_move(world_width, world_height)

    def _seek_building(self, economy, buildings: List[Building], b_type_name: str):
        targets = [b for b in buildings if b.type.value == b_type_name]
        if not targets:
            self.state.current_goal = "lost"
            return

        # Manhattan distance
        target = min(targets, key=lambda b: abs(b.pos.x - self.state.pos.x) + abs(b.pos.y - self.state.pos.y))
        
        if self.state.pos.x == target.pos.x and self.state.pos.y == target.pos.y:
            target.enter(self.state.id)
            self._perform_activity(economy, target)
        else:
            # Ensure they exit any building they were in if they are moving
            for b in buildings:
                b.exit(self.state.id)
            self._move_towards(target.pos)

    def _move_towards(self, target_pos: Position):
        if self.state.pos.x < target_pos.x: self.state.pos.x += 1
        elif self.state.pos.x > target_pos.x: self.state.pos.x -= 1
        elif self.state.pos.y < target_pos.y: self.state.pos.y += 1
        elif self.state.pos.y > target_pos.y: self.state.pos.y -= 1
        
        self.state.energy = max(0.0, self.state.energy - 0.5)

    def _random_move(self, w: int, h: int):
        dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1), (0,0)])
        self.state.pos.x = max(0, min(w - 1, self.state.pos.x + dx))
        self.state.pos.y = max(0, min(h - 1, self.state.pos.y + dy))
        self.state.energy = max(0.0, self.state.energy - 0.2)

    def _perform_activity(self, economy, building: Building):
        b_type = building.type.value
        if b_type == "home":
            self.state.energy = min(100.0, self.state.energy + 20.0)
        elif b_type == "office":
            income = 15.0
            self.state.wealth += income
            self.state.energy = max(0.0, self.state.energy - 10.0)
            economy.ledger.record("CITY_TREASURY", self.state.id, income, "salary")
        elif b_type == "market":
            cost = 10.0
            if self.state.wealth >= cost:
                self.state.wealth -= cost
                self.state.energy = min(100.0, self.state.energy + 40.0)
                economy.ledger.record(self.state.id, "MARKET_OWNER", cost, "groceries")