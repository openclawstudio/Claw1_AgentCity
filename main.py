import asyncio
from core.world import World
from core.agent import Citizen
from core.models import Position

async def main():
    # Initialize World
    city = World(width=50, height=50)
    
    # Seed initial citizens
    names = ["Alice", "Bob", "Charlie", "Dave"]
    for name in names:
        citizen = Citizen(
            name=name, 
            position=Position(x=25, y=25)
        )
        city.add_entity(citizen)

    print("--- AgentCity Simulation Starting ---")
    try:
        await city.start()
    except KeyboardInterrupt:
        city.running = False
        print("\n--- AgentCity Simulation Stopped ---")

if __name__ == "__main__":
    asyncio.run(main())