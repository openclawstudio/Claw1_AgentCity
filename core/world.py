import asyncio
import logging
from typing import Dict, List
from .models import Position, Entity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("World")

class World:
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.entities: Dict[str, Entity] = {}
        self.tick_rate = 1.0  # Seconds per tick
        self.running = False

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity
        logger.info(f"Entity {entity.id} spawned at {entity.position}")

    async def start(self):
        self.running = True
        tick_count = 0
        while self.running:
            await self.update()
            tick_count += 1
            if tick_count % 10 == 0:
                logger.info(f"World Heartbeat: Tick {tick_count}")
            await asyncio.sleep(self.tick_rate)

    async def update(self):
        for entity in self.entities.values():
            await entity.update(self)