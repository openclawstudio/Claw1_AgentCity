from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    item: Optional[str] = None
    timestamp: int