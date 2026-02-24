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

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

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
    inventory: List[Resource] = Field(default_factory=list)
    current_job: Optional[str] = None
    status_message: str = "Idle"

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    service_type: str
    timestamp: int