import random
from typing import Dict, List
from .models import Position, ZoneType

class Cell:
    def __init__(self, x: int, y: int):
        self.pos = Position(x=x, y=y)
        self.zone = ZoneType.OPEN_SPACE
        self.agents: List[str] = []

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.ticks = 0
        self._apply_zoning()

    def _apply_zoning(self):
        # Simple procedural zoning for MVP
        for x in range(self.width):
            for y in range(self.height):
                if x < self.width // 3:
                    self.grid[x][y].zone = ZoneType.RESIDENTIAL
                elif x < 2 * self.width // 3:
                    self.grid[x][y].zone = ZoneType.COMMERCIAL
                else:
                    self.grid[x][y].zone = ZoneType.INDUSTRIAL

    def get_cell(self, pos: Position) -> Cell:
        return self.grid[pos.x][pos.y]

    def tick(self):
        self.ticks += 1