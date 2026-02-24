from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from enum import Enum

class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    EMPTY = "empty"

class Transaction(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    purpose: str
    timestamp: int

class Offer(BaseModel):
    id: str
    creator_id: str
    item: str
    price: float
    quantity: int

class AgentState(BaseModel):
    id: str
    pos: Tuple[int, int]
    energy: float = 100.0
    wallet: float = 50.0
    job_role: Optional[str] = None
    inventory: Dict[str, int] = {}