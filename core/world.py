import asyncio
import logging
from typing import Dict, List, Any
from .models import Position, Entity
from .config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("World")

class World:
    def __init__(self, width: int = None, height: int = None):
        self.width = width or settings.WORLD_WIDTH
        self.height = height or settings.WORLD_HEIGHT
        self.entities: Dict[str, Entity] = {}
        self.tick_rate = settings.TICK_RATE
        self.running = False
        self._tick_count = 0

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity
        logger.info(f"Entity {entity.name} ({entity.id}) spawned at {entity.position}")

    async def start(self):
        self.running = True
        logger.info("World started.")
        try:
            while self.running:
                await self.update()
                self._tick_count += 1
                if self._tick_count % 10 == 0:
                    logger.info(f"World Heartbeat: Tick {self._tick_count} | Entities: {len(self.entities)}")
                await asyncio.sleep(self.tick_rate)
        except asyncio.CancelledError:
            self.running = False
            logger.info("World execution cancelled.")

    async def update(self):
        # Use asyncio.gather for concurrent entity updates
        tasks = [entity.update(self) for entity in self.entities.values()]
        if tasks:
            await asyncio.gather(*tasks)

    def stop(self):
        self.running = False
        logger.info("Stopping world...")