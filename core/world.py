import random
from typing import Dict, List, Tuple, TYPE_CHECKING
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
                # Basic procedural zoning
                if (x + y) % 5 == 0:
                    zt = ZoneType.COMMERCIAL
                elif (x * y) % 4 == 0:
                    zt = ZoneType.INDUSTRIAL
                else:
                    zt = ZoneType.RESIDENTIAL
                
                self.grid[(x, y)] = zt
                self._zone_cache[zt].append((x, y))

    def get_zone(self, pos: Position) -> ZoneType:
        return self.grid.get((pos.x, pos.y), ZoneType.OPEN_SPACE)

    def get_nearest_zone(self, pos: Position, zone_type: ZoneType) -> Position:
        coords = self._zone_cache.get(zone_type, [])
        if not coords:
            return pos
        
        # Find nearest coordinate using Manhattan distance
        best_coord = min(coords, key=lambda c: abs(c[0] - pos.x) + abs(c[1] - pos.y))
        return Position(x=best_coord[0], y=best_coord[1])

    def add_agent(self, agent: 'Citizen'):
        self.agents[agent.id] = agent

    def record_transaction(self, tx: Transaction):
        self.ledger.append(tx)

    def step(self):
        self.tick_counter += 1
        # Use a list to avoid dictionary mutation issues during iteration if agents are added/removed
        for agent in list(self.agents.values()):
            agent.step(self)