from pydantic import BaseModel
from typing import List, Optional, Tuple

class Position(BaseModel):
    x: int
    y: int

class Transaction(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    amount: float
    purpose: str
    timestamp: str

class AgentState(BaseModel):
    id: str
    name: str
    pos: Position
    energy: float = 100.0
    wealth: float = 50.0
    inventory: List[str] = []
    current_goal: Optional[str] = "idle"