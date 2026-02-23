import asyncio
import signal
import logging
import sys
from core.world import World
from core.agent import Citizen
from core.models import Position, Resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

async def main():
    city = World(width=50, height=50)
    
    # Add static food sources (Resources)
    food_source = Resource(name="Market", position=Position(x=25, y=25), value=30)
    city.add_entity(food_source)
    
    # Seed citizens
    names = ["Alice", "Bob", "Charlie", "Dave"]
    for i, name in enumerate(names):
        citizen = Citizen(
            name=name, 
            position=Position(x=10 + i*5, y=10 + i*5)
        )
        city.add_entity(citizen)

    print("--- AgentCity Simulation Starting ---")
    
    stop_event = asyncio.Event()
    def ask_exit():
        stop_event.set()

    if sys.platform != "win32":
        loop = asyncio.get_running_loop()
        for s in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(s, ask_exit)
    
    simulation_task = asyncio.create_task(city.start())
    
    try:
        while not stop_event.is_set():
            await asyncio.sleep(1)
            if not city.running:
                break
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        city.stop()
        simulation_task.cancel()
        try: await simulation_task
        except asyncio.CancelledError: pass
        print("\n--- AgentCity Simulation Stopped ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt: pass