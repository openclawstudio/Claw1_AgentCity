import asyncio
import logging
from typing import Dict, List, Any, Optional
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
        logger.info(f"Entity {entity.name} ({entity.id}) joined the world at {entity.position}")

    def remove_entity(self, entity_id: str):
        if entity_id in self.entities:
            del self.entities[entity_id]

    def get_nearby_entities(self, pos: Position, radius: int = 5) -> List[Entity]:
        nearby = []
        for e in self.entities.values():
            if abs(e.position.x - pos.x) <= radius and abs(e.position.y - pos.y) <= radius:
                nearby.append(e)
        return nearby

    async def start(self):
        self.running = True
        logger.info("World started.")
        try:
            while self.running:
                await self.update()
                self._tick_count += 1
                if self._tick_count % 10 == 0:
                    active_count = sum(1 for e in self.entities.values() if e.active)
                    logger.info(f"World Heartbeat: Tick {self._tick_count} | Entities: {len(self.entities)} ({active_count} active)")
                await asyncio.sleep(self.tick_rate)
        except asyncio.CancelledError:
            self.running = False
            logger.info("World execution cancelled.")
        except Exception as e:
            logger.error(f"Critical World Error: {e}", exc_info=True)
            self.running = False

    async def update(self):
        # Snapshot keys to avoid dictionary size change during iteration
        entity_ids = list(self.entities.keys())
        tasks = []
        
        for eid in entity_ids:
            entity = self.entities.get(eid)
            if entity and entity.active:
                tasks.append(entity.update(self))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    logger.error(f"Entity update error: {res}")

    def stop(self):
        self.running = False
        logger.info("Stopping world...")