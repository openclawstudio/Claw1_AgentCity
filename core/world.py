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

    def get_nearby_entities(self, pos: Position, radius: int = 5) -> List[Entity]:
        """Basic spatial query"""
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
            logger.error(f"Critical World Error: {e}")
            self.running = False

    async def update(self):
        # Create a list of current entities to avoid dict mutation issues during update
        current_entities = list(self.entities.values())
        if not current_entities:
            return
            
        results = await asyncio.gather(
            *[entity.update(self) for entity in current_entities if entity.active],
            return_exceptions=True
        )
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"Update failed for an entity: {res}")

    def stop(self):
        self.running = False
        logger.info("Stopping world...")