from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
import uuid

class Position(BaseModel):
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: Position
    energy: float = 100.0
    balance: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    active: bool = True
    kind: str = "entity"

    async def update(self, world: Any):
        """Base update logic for all entities"""
        pass

class Resource(Entity):
    kind: str = "resource"
    value: float = 20.0
    depleted: bool = False