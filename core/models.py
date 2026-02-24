from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class EntityType(str, Enum):
    CITIZEN = "citizen"
    BUSINESS = "business"
    INFRASTRUCTURE = "infrastructure"

class ResourceType(str, Enum):
    CREDITS = "credits"
    ENERGY = "energy"
    FOOD = "food"
    SERVICE = "service"

class Position(BaseModel):
    x: int
    y: int

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    resource_type: ResourceType
    timestamp: int

class Job(BaseModel):
    job_id: str
    employer_id: str
    title: str
    salary: float
    requirements: Dict[str, float]

class AgentState(BaseModel):
    id: str
    pos: Position
    energy: float = 100.0
    balance: float = 50.0
    inventory: Dict[str, float] = {}
    profession: Optional[str] = None

class BusinessState(BaseModel):
    id: str
    pos: Position
    business_type: str
    balance: float = 0.0
    employees: List[str] = []