import random
from typing import List, Optional, TYPE_CHECKING
from core.models import AgentState, Position
from core.entity import Building, BuildingType

if TYPE_CHECKING:
    from core.economy import EconomySystem

class CitizenAgent:
    """An autonomous AI agent with needs, goals, and economic capacity."""
    def __init__(self, id: str, name: str, pos: Position):
        self.state = AgentState(id=id, name=name, pos=pos)

    def decide(self, economy: 'EconomySystem', buildings: List[Building], world_width: int, world_height: int):
        """Main decision logic based on internal utility."""
        # Determine move target or activity
        if self.state.energy < 20:
            self.state.current_goal = "rest"
            return self._seek_building(economy, buildings, BuildingType.HOME, world_width, world_height)
        
        if self.state.wealth < 15:
            self.state.current_goal = "work"
            return self._seek_building(economy, buildings, BuildingType.OFFICE, world_width, world_height)

        if self.state.wealth >= 30 and self.state.energy < 70:
            self.state.current_goal = "shop"
            return self._seek_building(economy, buildings, BuildingType.MARKET, world_width, world_height)

        self.state.current_goal = "explore"
        return self._random_move(world_width, world_height)

    def _seek_building(self, economy: 'EconomySystem', buildings: List[Building], b_type: BuildingType, w: int, h: int):
        targets = [b for b in buildings if b.type == b_type]
        if not targets:
            self.state.current_goal = "wandering (no targets)"
            return self._random_move(w, h)

        # Manhattan distance
        target = min(targets, key=lambda b: abs(b.pos.x - self.state.pos.x) + abs(b.pos.y - self.state.pos.y))
        
        if self.state.pos.x == target.pos.x and self.state.pos.y == target.pos.y:
            if self.state.id not in target.occupants:
                target.enter(self.state.id)
            self._perform_activity(economy, target)
        else:
            # If moving, ensure we exit any building we might be in
            for b in buildings:
                if self.state.id in b.occupants:
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

    def _perform_activity(self, economy: 'EconomySystem', building: Building):
        if building.type == BuildingType.HOME:
            self.state.energy = min(100.0, self.state.energy + 20.0)
        elif building.type == BuildingType.OFFICE:
            income = 15.0
            self.state.wealth += income
            self.state.energy = max(0.0, self.state.energy - 10.0)
            economy.ledger.record("CITY_TREASURY", self.state.id, income, "salary")
        elif building.type == BuildingType.MARKET:
            cost = 10.0
            if self.state.wealth >= cost:
                self.state.wealth -= cost
                self.state.energy = min(100.0, self.state.energy + 40.0)
                economy.ledger.record(self.state.id, "MARKET_OWNER", cost, "groceries")