import random
from typing import Dict, List, Tuple, TYPE_CHECKING, Optional
from core.models import Position, ZoneType, Transaction

if TYPE_CHECKING:
    from core.agent import Citizen

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: Dict[Tuple[int, int], ZoneType] = {}
        self.agents: Dict[str, 'Citizen'] = {}
        self.tick_counter = 0
        self.ledger: List[Transaction] = []
        self._zone_cache: Dict[ZoneType, List[Tuple[int, int]]] = {z: [] for z in ZoneType}
        self._initialize_zones()

    def _initialize_zones(self):
        for x in range(self.width):
            for y in range(self.height):
                # Use a pseudo-random but deterministic distribution
                val = random.random()
                if val < 0.15:
                    zt = ZoneType.COMMERCIAL
                elif val < 0.30:
                    zt = ZoneType.INDUSTRIAL
                elif val < 0.50:
                    zt = ZoneType.OPEN_SPACE
                else:
                    zt = ZoneType.RESIDENTIAL
                self.set_zone(x, y, zt)
        
        # Safety check: ensure at least one of each functional zone exists
        for zt in [ZoneType.RESIDENTIAL, ZoneType.COMMERCIAL, ZoneType.INDUSTRIAL]:
            if not self._zone_cache[zt]:
                rx, ry = random.randint(0, self.width-1), random.randint(0, self.height-1)
                self.set_zone(rx, ry, zt)

    def set_zone(self, x: int, y: int, zone_type: ZoneType):
        pos_tuple = (x, y)
        if pos_tuple in self.grid:
            old_zone = self.grid[pos_tuple]
            if old_zone == zone_type:
                return
            if pos_tuple in self._zone_cache[old_zone]:
                self._zone_cache[old_zone].remove(pos_tuple)
            
        self.grid[pos_tuple] = zone_type
        self._zone_cache[zone_type].append(pos_tuple)

    def get_zone(self, pos: Position) -> ZoneType:
        return self.grid.get((pos.x, pos.y), ZoneType.OPEN_SPACE)

    def get_nearest_zone(self, pos: Position, zone_type: ZoneType) -> Position:
        coords = self._zone_cache.get(zone_type, [])
        if not coords:
            return Position(x=random.randint(0, self.width-1), y=random.randint(0, self.height-1))
        
        best_coord = min(coords, key=lambda c: abs(c[0] - pos.x) + abs(c[1] - pos.y))
        return Position(x=best_coord[0], y=best_coord[1])

    def add_agent(self, agent: 'Citizen'):
        self.agents[agent.id] = agent

    def record_transaction(self, tx: Transaction):
        self.ledger.append(tx)

    def step(self):
        self.tick_counter += 1
        agent_list = list(self.agents.values())
        random.shuffle(agent_list)
        for agent in agent_list:
            agent.step(self)