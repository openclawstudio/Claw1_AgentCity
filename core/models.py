from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    OPEN_SPACE = "open_space"

class ResourceType(str, Enum):
    CURRENCY = "credits"
    ENERGY = "energy"
    MATERIALS = "materials"
    FOOD = "food"

class Position(BaseModel):
    x: int
    y: int

class InventoryItem(BaseModel):
    type: ResourceType
    amount: float

class Job(BaseModel):
    id: str
    employer_id: str
    title: str
    payout: float
    energy_cost: float
    location: Position
    completed: bool = False

class AgentState(BaseModel):
    id: str
    name: str
    pos: Position
    energy: float = 100.0
    balance: float = 0.0
    inventory: List[InventoryItem] = []
    current_goal: Optional[str] = None