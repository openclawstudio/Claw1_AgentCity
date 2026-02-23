import asyncio
import uuid
import logging
import random
from core.world import World
from core.agent import CitizenAgent
from core.models import AgentState, Vector2D

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("Main")

async def main():
    city = World(50, 50)
    
    # Spawn initial citizens
    agents = []
    for i in range(10):
        state = AgentState(
            id=str(uuid.uuid4())[:8],
            name=f"Citizen_{i}",
            position=Vector2D(x=random.randint(0, 49), y=random.randint(0, 49))
        )
        city.add_agent(state)
        agents.append(CitizenAgent(state))

    print("\n--- AgentCity MVP Starting ---")
    print(f"Initialized city with {len(agents)} agents.\n")
    
    try:
        for tick in range(100):
            # 1. Update World Physics/Rules
            await city.tick()
            
            # 2. Run Agents in Parallel
            # As we scale, we'd use a task queue, but gather is sufficient for this stage.
            tasks = [agent.decide_action(city) for agent in agents]
            await asyncio.gather(*tasks)
            
            # 3. Reporting
            if tick % 10 == 0:
                active_agents = [a for a in agents if a.state.energy > 0]
                print(f"Tick {tick} | Active: {len(active_agents)} | Ledger Entries: {len(city.ledger.history)}")
                if active_agents:
                    lead = active_agents[0]
                    zone = city.get_zone(lead.state.position)
                    print(f"  Status Check: {lead.state.name} at {lead.state.position} [{zone}] | E: {lead.state.energy:.1f} | $: {lead.state.economy.balance}")
            
            await asyncio.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        logger.exception(f"Simulation crashed: {e}")
    finally:
        print("--- Simulation Terminated ---")

if __name__ == "__main__":
    asyncio.run(main())