import enum
from core.models import Position

class BuildingType(enum.Enum):
    HOME = "home"
    OFFICE = "office"
    MARKET = "market"
    LAB = "lab"

class Building:
    def __init__(self, id: str, b_type: BuildingType, pos: Position):
        self.id = id
        self.type = b_type
        self.pos = pos
        self.occupants = []

    def enter(self, agent_id: str):
        self.occupants.append(agent_id)

    def exit(self, agent_id: str):
        if agent_id in self.occupants:
            self.occupants.remove(agent_id)