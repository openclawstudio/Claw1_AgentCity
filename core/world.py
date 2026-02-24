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
                # Deterministic but varied zoning
                val = (x * 3 + y * 7)
                if val % 10 == 0:
                    zt = ZoneType.COMMERCIAL
                elif val % 10 == 1:
                    zt = ZoneType.INDUSTRIAL
                elif val % 10 in [2, 3]:
                    zt = ZoneType.OPEN_SPACE
                else:
                    zt = ZoneType.RESIDENTIAL
                
                self.set_zone(x, y, zt)
        
        # Safety check: Ensure at least one of each critical zone exists
        for zt in [ZoneType.RESIDENTIAL, ZoneType.COMMERCIAL, ZoneType.INDUSTRIAL]:
            if not self._zone_cache[zt]:
                rx, ry = random.randint(0, self.width-1), random.randint(0, self.height-1)
                self.set_zone(rx, ry, zt)

    def set_zone(self, x: int, y: int, zone_type: ZoneType):
        old_zone = self.grid.get((x, y))
        if old_zone == zone_type:
            return
        
        if old_zone and (x, y) in self._zone_cache[old_zone]:
            self._zone_cache[old_zone].remove((x, y))
            
        self.grid[(x, y)] = zone_type
        self._zone_cache[zone_type].append((x, y))

    def get_zone(self, pos: Position) -> ZoneType:
        return self.grid.get((pos.x, pos.y), ZoneType.OPEN_SPACE)

    def get_nearest_zone(self, pos: Position, zone_type: ZoneType) -> Position:
        coords = self._zone_cache.get(zone_type, [])
        if not coords:
            # Fallback to random if no zone exists (should not happen with safety check)
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