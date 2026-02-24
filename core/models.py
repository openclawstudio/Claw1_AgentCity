from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    OPEN_SPACE = "open_space"

class Position(BaseModel):
    x: int
    y: int

class Wallet(BaseModel):
    balance: float = 0.0
    currency: str = "CLAW"

class Resource(BaseModel):
    name: str
    amount: float

class AgentState(BaseModel):
    energy: float = 100.0
    happiness: float = 100.0
    wallet: Wallet = Field(default_factory=Wallet)
    inventory: List[Resource] = []
    current_job: Optional[str] = None

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    service_type: str
    timestamp: int