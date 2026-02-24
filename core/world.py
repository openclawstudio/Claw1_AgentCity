import random
from typing import List, Dict
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
        self._initialize_grid()

    def _initialize_grid(self):
        zones = list(ZoneType)
        for x in range(self.width):
            for y in range(self.height):
                key = f"{x},{y}"
                zone = random.choice(zones)
                self.grid[key] = Cell(Position(x=x, y=y), zone)

    def get_cell(self, pos: Position) -> Cell:
        return self.grid.get(f"{pos.x},{pos.y}")

    def tick(self):
        for agent in self.agents:
            # Natural energy decay
            agent.energy -= 0.5
            # Apply zone-based effects
            cell = self.get_cell(agent.pos)
            if cell.zone == ZoneType.RESIDENTIAL:
                agent.energy = min(100.0, agent.energy + 2.0)
            elif cell.zone == ZoneType.INDUSTRIAL:
                agent.energy -= 1.0