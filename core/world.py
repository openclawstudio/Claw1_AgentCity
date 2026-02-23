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
        except Exception as e:
            logger.error(f"Critical World Error: {e}")
            self.running = False

    async def update(self):
        if not self.entities:
            return
            
        # Use return_exceptions=True to prevent one agent's failure from stopping the world
        results = await asyncio.gather(
            *[entity.update(self) for entity in self.entities.values()],
            return_exceptions=True
        )
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                entity_id = list(self.entities.keys())[i]
                logger.error(f"Entity {entity_id} failed update: {res}")

    def stop(self):
        self.running = False
        logger.info("Stopping world...")