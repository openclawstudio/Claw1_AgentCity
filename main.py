import asyncio
import uuid
import logging
import random
from core.world import World
from core.agent import CitizenAgent, BusinessAgent
from core.models import AgentState, Vector2D, EntityType, SimulationConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("Main")

async def main():
    config = SimulationConfig(width=50, height=50)
    city = World(config)
    
    # 1. Spawn Critical Businesses (Infrastructure)
    # Food Hub in the Market
    market_pos = Vector2D(x=25, y=25)
    biz_state = AgentState(
        id="market_stall_1",
        name="Market Deli",
        position=market_pos,
        type=EntityType.BUSINESS,
        metadata={"service_type": "food"}
    )
    city.add_agent(biz_state)
    
    # Job Board / Town Hall
    hall_state = AgentState(
        id="town_hall",
        name="Citizen Center",
        position=Vector2D(x=20, y=20),
        type=EntityType.BUSINESS,
        metadata={"service_type": "job_board"}
    )
    city.add_agent(hall_state)

    # 2. Spawn Citizens
    agents = []
    for i in range(12):
        state = AgentState(
            id=str(uuid.uuid4())[:8],
            name=f"Citizen_{i}",
            position=Vector2D(x=random.randint(0, 49), y=random.randint(0, 49))
        )
        # Give initial capital
        state.economy.balance = random.uniform(10.0, 30.0)
        city.add_agent(state)
        agents.append(CitizenAgent(state))

    print("\n--- AgentCity MVP Starting ---")
    print(f"Initialized city with {len(agents)} citizens and {len(city.services)} service types.\n")
    
    try:
        for tick in range(200): 
            # 1. Update World Physics/Rules
            await city.tick()
            
            # 2. Run Agents
            tasks = [agent.decide_action(city) for agent in agents]
            await asyncio.gather(*tasks)
            
            # 3. Reporting
            if tick % 20 == 0:
                active_agents = [a for a in agents if a.state.energy > 0]
                avg_bal = sum(a.state.economy.balance for a in agents) / len(agents)
                print(f"Tick {tick:03d} | Active: {len(active_agents)} | Avg $: {avg_bal:.2f} | TXs: {len(city.ledger.history)}")
                if active_agents:
                    lead = random.choice(active_agents)
                    zone = city.get_zone(lead.state.position)
                    print(f"  [Spotlight] {lead.state.name} at {lead.state.position} in {zone} (E: {lead.state.energy:.1f})")
            
            await asyncio.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        logger.exception(f"Simulation crashed: {e}")
    finally:
        print("--- Simulation Terminated ---")

if __name__ == "__main__":
    asyncio.run(main())