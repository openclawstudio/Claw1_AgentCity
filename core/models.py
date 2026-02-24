from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ResourceType(str, Enum):
    ENERGY = "energy"
    DATA = "data"
    MATERIALS = "materials"
    CREDITS = "credits"

class Position(BaseModel):
    x: int
    y: int

class InventoryItem(BaseModel):
    resource_type: ResourceType
    amount: float

class AgentState(BaseModel):
    id: str
    name: str
    position: Position
    inventory: Dict[ResourceType, float] = {}
    energy_level: float = 100.0
    status: str = "idle"

class WorldState(BaseModel):
    tick: int
    agents: List[AgentState]
    market_prices: Dict[ResourceType, float]
