from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict

class Position(BaseModel):
    x: int
    y: int

class AgentState(BaseModel):
    id: str
    name: str
    pos: Position
    energy: float = 100.0
    wallet: float = 50.0
    inventory: Dict[str, int] = {}
    profession: str = "UNEMPLOYED"
    current_goal: Optional[str] = None

class DistrictType(BaseModel):
    name: str
    color: str
    description: str
    multiplier: float = 1.0

class District(BaseModel):
    type: str
    area: List[Tuple[int, int]]

class WorldState(BaseModel):
    width: int
    height: int
    tick: int = 0
    agents: List[AgentState] = []
    districts: List[District] = []