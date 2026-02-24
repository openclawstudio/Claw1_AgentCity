import enum
from typing import Set
from core.models import Position

class BuildingType(enum.Enum):
    HOME = "home"
    OFFICE = "office"
    MARKET = "market"
    LAB = "lab"

class Building:
    """Represents a physical structure in the grid where agents perform tasks."""
    def __init__(self, id: str, b_type: BuildingType, pos: Position):
        self.id = id
        self.type = b_type
        self.pos = pos
        self.occupants: Set[str] = set()

    def enter(self, agent_id: str):
        self.occupants.add(agent_id)

    def exit(self, agent_id: str):
        self.occupants.discard(agent_id)