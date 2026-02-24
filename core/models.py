from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class Role(str, Enum):
    CITIZEN = "citizen"
    ENTREPRENEUR = "entrepreneur"
    WORKER = "worker"
    GOVERNMENT = "government"

class ResourceType(str, Enum):
    ENERGY = "energy"
    CREDITS = "credits"
    MATERIALS = "materials"

class InventoryItem(BaseModel):
    name: str
    quantity: float
    unit_price: Optional[float] = 0.0

class AgentState(BaseModel):
    id: str
    pos: tuple[int, int]
    role: Role = Role.CITIZEN
    energy: float = 100.0
    balance: float = 500.0
    inventory: List[InventoryItem] = []
    memory: List[str] = []

class BusinessState(BaseModel):
    id: str
    owner_id: str
    pos: tuple[int, int]
    business_type: str
    employees: List[str] = []
    vault: float = 0.0