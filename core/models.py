from pydantic import BaseModel, Field
from typing import Optional, List, Any
import uuid

class Position(BaseModel):
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: Position
    energy: float = 100.0
    balance: float = 0.0

    async def update(self, world: Any):
        """Base update logic for all entities"""
        pass