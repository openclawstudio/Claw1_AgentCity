import random
from typing import Dict, Tuple, List, Optional
from .models import ZoneType
from .economy import EconomyManager

from .market import Market

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.zones: Dict[Tuple[int, int], ZoneType] = {}
        self.agents = []
        self.agent_map = {}
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

    def get_zones_by_type(self, zone_type: ZoneType) -> List[Tuple[int, int]]:
        return [pos for pos, zt in self.zones.items() if zt == zone_type]

    def step(self):
        self.tick_count += 1
        
        # 1. Update fast-lookup map for the current tick
        self.agent_map = {a.id: a for a in self.agents if a.alive}
        
        # 2. Cleanup market (remove offers from dead agents)
        self.market.cleanup_stale_offers(set(self.agent_map.keys()))
        
        # 3. Perform actions
        for agent in self.agents:
            if agent.alive:
                agent.step(self)
        
        # 4. Cleanup dead agents from simulation
        self.agents = [a for a in self.agents if a.alive]