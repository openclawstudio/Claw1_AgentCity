from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    WILDERNESS = "wilderness"

class ResourceType(str, Enum):
    ENERGY = "energy"
    CURRENCY = "currency"
    MATERIALS = "materials"
    KNOWLEDGE = "knowledge"

class Position(BaseModel):
    x: int
    y: int

class AgentState(BaseModel):
    id: str
    name: str
    pos: Position
    energy: float = 100.0
    wallet: float = 50.0
    inventory: Dict[str, float] = {}
    profession: str = "unemployed"
    last_action: str = "idle"