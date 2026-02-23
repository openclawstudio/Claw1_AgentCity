import asyncio
import uuid
import logging
from core.world import World
from core.agent import CitizenAgent
from core.models import AgentState, Vector2D

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

async def main():
    city = World(50, 50)
    
    # Spawn initial citizens
    agents = []
    for i in range(5):
        state = AgentState(
            id=str(uuid.uuid4())[:8],
            name=f"Citizen_{i}",
            position=Vector2D(x=random.randint(0,49), y=random.randint(0,49)) if 'random' in globals() else Vector2D(x=10, y=10)
        )
        city.add_agent(state)
        agents.append(CitizenAgent(state))

    print("--- AgentCity MVP Starting ---")
    
    try:
        for tick in range(100):
            await city.tick()
            
            # Sequential decision making for MVP
            for agent in agents:
                try:
                    await agent.decide_action(city)
                except Exception as e:
                    logger.error(f"Error processing agent {agent.state.id}: {e}")
            
            if tick % 10 == 0:
                print(f"\nTick {tick}: {len(city.agents)} agents active.")
                for a in agents:
                    zone = city.get_zone(a.state.position)
                    print(f"  {a.state.name} @ ({a.state.position.x},{a.state.position.y}) [{zone}] | E: {a.state.energy:.1f} | $: {a.state.economy.balance}")
            
            await asyncio.sleep(0.05)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    import random # Ensure random is available for initialization
    asyncio.run(main())