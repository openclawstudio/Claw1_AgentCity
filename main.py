import asyncio
import signal
import logging
from core.world import World
from core.agent import Citizen
from core.models import Position

# Configure logging
logging.basicConfig(level=logging.INFO)

async def shutdown(loop, world, signal=None):
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    world.stop()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    loop = asyncio.get_running_loop()
    city = World(width=50, height=50)
    
    # Register signals for graceful shutdown
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(loop, city, signal=s)))

    # Seed initial citizens
    names = ["Alice", "Bob", "Charlie", "Dave"]
    for i, name in enumerate(names):
        citizen = Citizen(
            name=name, 
            position=Position(x=20 + i, y=20 + i)
        )
        city.add_entity(citizen)

    print("--- AgentCity Simulation Starting ---")
    try:
        await city.start()
    except asyncio.CancelledError:
        pass
    finally:
        print("\n--- AgentCity Simulation Stopped ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass