import random
from typing import Dict, List, Tuple
from core.models import Position, ZoneType, Transaction

class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: Dict[Tuple[int, int], ZoneType] = {}
        self.agents: Dict[str, any] = {}
        self.tick_counter = 0
        self.ledger: List[Transaction] = []
        self._initialize_zones()

    def _initialize_zones(self):
        for x in range(self.width):
            for y in range(self.height):
                # Basic procedural zoning
                if (x + y) % 5 == 0:
                    self.grid[(x, y)] = ZoneType.COMMERCIAL
                elif (x * y) % 4 == 0:
                    self.grid[(x, y)] = ZoneType.INDUSTRIAL
                else:
                    self.grid[(x, y)] = ZoneType.RESIDENTIAL

    def get_zone(self, pos: Position) -> ZoneType:
        return self.grid.get((pos.x, pos.y), ZoneType.OPEN_SPACE)

    def add_agent(self, agent):
        self.agents[agent.id] = agent

    def record_transaction(self, tx: Transaction):
        self.ledger.append(tx)

    def step(self):
        self.tick_counter += 1
        for agent in self.agents.values():
            agent.step(self)