from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ResourceType(str, Enum):
    ENERGY = "energy"
    DATA = "data"
    MATERIALS = "materials"
    CREDITS = "credits"

class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    REFUELING = "refueling"
    EXHAUSTED = "exhausted"
    BROKE = "broke"
    EXPLORING = "exploring"

class Position(BaseModel):
    x: int
    y: int

class AgentState(BaseModel):
    id: str
    name: str
    position: Position
    inventory: Dict[ResourceType, float] = Field(default_factory=lambda: {
        ResourceType.ENERGY: 0.0,
        ResourceType.DATA: 0.0,
        ResourceType.MATERIALS: 0.0,
        ResourceType.CREDITS: 0.0
    })
    energy_level: float = 100.0
    status: AgentStatus = AgentStatus.IDLE

class WorldState(BaseModel):
    tick: int
    agents: List[AgentState]
    market_prices: Dict[ResourceType, float]