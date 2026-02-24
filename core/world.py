import random
from typing import Dict, Tuple, List
from .models import ZoneType
from .economy import EconomyManager
from .market import Market

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.zones: Dict[Tuple[int, int], ZoneType] = {}
        self.agents = []
        self.tick_count = 0
        self.economy = EconomyManager()
        self.market = Market()
        self._initialize_zones()

    def _initialize_zones(self):
        for x in range(self.width):
            for y in range(self.height):
                choice = random.random()
                if choice < 0.1: self.zones[(x, y)] = ZoneType.COMMERCIAL
                elif choice < 0.2: self.zones[(x, y)] = ZoneType.INDUSTRIAL
                elif choice < 0.6: self.zones[(x, y)] = ZoneType.RESIDENTIAL
                else: self.zones[(x, y)] = ZoneType.EMPTY

    def get_zone(self, pos: Tuple[int, int]) -> ZoneType:
        return self.zones.get(pos, ZoneType.EMPTY)

    def step(self):
        self.tick_count += 1
        for agent in self.agents:
            agent.step(self)