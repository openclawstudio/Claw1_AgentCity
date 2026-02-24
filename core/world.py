import random
from typing import List, Dict, Optional
from .models import Position, ZoneType, AgentState

class Cell:
    def __init__(self, pos: Position, zone: ZoneType):
        self.pos = pos
        self.zone = zone
        self.resources = 100.0

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: Dict[str, Cell] = {}
        self.agents: List[AgentState] = []
        self._zone_cache: Dict[ZoneType, List[Position]] = {z: [] for z in ZoneType}
        self._initialize_grid()

    def _initialize_grid(self):
        zones = list(ZoneType)
        for x in range(self.width):
            for y in range(self.height):
                key = f"{x},{y}"
                zone = random.choice(zones)
                pos = Position(x=x, y=y)
                self.grid[key] = Cell(pos, zone)
                self._zone_cache[zone].append(pos)

    def get_cell(self, pos: Position) -> Optional[Cell]:
        return self.grid.get(f"{pos.x},{pos.y}")

    def find_nearest_zone(self, start_pos: Position, zone_type: ZoneType) -> Optional[Position]:
        targets = self._zone_cache.get(zone_type, [])
        if not targets:
            return None
        # Return closest via Manhattan distance
        return min(targets, key=lambda p: abs(p.x - start_pos.x) + abs(p.y - start_pos.y))

    def tick(self):
        for agent in self.agents:
            # Natural energy decay
            agent.energy -= 0.5
            
            # Apply zone-based effects
            cell = self.get_cell(agent.pos)
            if cell:
                if cell.zone == ZoneType.RESIDENTIAL:
                    agent.energy = min(100.0, agent.energy + 2.5)
                elif cell.zone == ZoneType.INDUSTRIAL:
                    agent.energy -= 0.5
            
            # Ensure energy doesn't go negative
            agent.energy = max(0.0, agent.energy)