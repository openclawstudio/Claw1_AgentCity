from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class EntityType(str, Enum):
    CITIZEN = "citizen"
    BUSINESS = "business"
    INFRASTRUCTURE = "infrastructure"

class JobStatus(str, Enum):
    UNEMPLOYED = "unemployed"
    EMPLOYED = "employed"
    BUSINESS_OWNER = "business_owner"

class Vector2D(BaseModel):
    x: int
    y: int

    def distance_to(self, other: 'Vector2D') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

class EconomicState(BaseModel):
    balance: float = 0.0
    inventory: Dict[str, int] = {}
    job_status: JobStatus = JobStatus.UNEMPLOYED
    employer_id: Optional[str] = None

class AgentState(BaseModel):
    id: str
    name: str
    position: Vector2D
    energy: float = 100.0
    economy: EconomicState = Field(default_factory=EconomicState)
    type: EntityType = EntityType.CITIZEN
    metadata: Dict[str, Any] = {}

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    item: Optional[str] = None
    timestamp: int

class SimulationConfig(BaseModel):
    width: int = 50
    height: int = 50
    max_ticks: int = 1000
    energy_decay: float = 0.5
    recovery_rate: float = 3.0