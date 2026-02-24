from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class Profession(str, Enum):
    UNEMPLOYED = "unemployed"
    EXTRACTOR = "extractor"  # Gathers raw resources
    REFINER = "refiner"      # Processes resources
    MERCHANT = "merchant"    # Facilitates trade

class ResourceType(str, Enum):
    ENERGY = "energy"
    MATERIALS = "materials"
    CURRENCY = "currency"

class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class MarketOrder(BaseModel):
    id: str
    agent_id: str
    resource: ResourceType
    order_type: OrderType
    quantity: float
    price: float
    timestamp: int

class AgentState(BaseModel):
    id: str
    pos_x: int
    pos_y: int
    energy: float = 100.0
    inventory: Dict[ResourceType, float] = {ResourceType.CURRENCY: 100.0}
    profession: Profession = Profession.UNEMPLOYED
    goals: List[str] = []