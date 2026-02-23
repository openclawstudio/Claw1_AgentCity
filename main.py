import asyncio
import uuid
from core.world import World
from core.agent import CitizenAgent
from core.models import AgentState, Vector2D

async def main():
    city = World(50, 50)
    
    # Spawn initial citizens
    agents = []
    for i in range(5):
        state = AgentState(
            id=str(uuid.uuid4())[:8],
            name=f"Citizen_{i}",
            position=Vector2D(x=25, y=25)
        )
        city.add_agent(state)
        agents.append(CitizenAgent(state))

    print("--- AgentCity MVP Starting ---")
    
    try:
        for tick in range(100):
            await city.tick()
            for agent in agents:
                agent.decide_action(city)
            
            if tick % 10 == 0:
                print(f"Tick {tick}: {len(city.agents)} agents active.")
                for a in agents:
                    print(f"  {a.state.name}: Pos({a.state.position.x},{a.state.position.y}) | Energy: {a.state.energy:.1f} | Balance: ${a.state.economy.balance}")
            
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    asyncio.run(main())