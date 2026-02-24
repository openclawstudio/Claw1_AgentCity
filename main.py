import time
import random
import uuid
from core.world import World
from core.agent import Citizen
from core.market import Market
from core.economy import EconomyManager
from core.models import Position, Job

def run_simulation():
    print("--- Starting AgentCity MVP ---")
    world = World(10, 10)
    market = Market()
    economy = EconomyManager()
    
    # Spawn agents
    citizens = []
    for i in range(5):
        pos = Position(x=random.randint(0,9), y=random.randint(0,9))
        agent = Citizen(f"Agent_{i}", pos)
        citizens.append(agent)
        # Register agent in world cell
        world.get_cell(pos).agents.append(agent.id)

    # Add initial liquidity/jobs
    market.job_board.post_job(Job(
        id=str(uuid.uuid4()),
        employer_id="SYSTEM",
        title="Factory Shift",
        payout=50.0,
        energy_cost=20.0,
        location=Position(x=8, y=5)
    ))

    try:
        for tick in range(50):
            world.tick()
            print(f"\nTick {tick} | GDP: {economy.global_gdp:.2f} | Jobs Available: {len(market.job_board.available_jobs)}")
            
            for agent in citizens:
                agent.step(market, economy, world)
                print(f"[{agent.state.current_goal}] {agent.state.name}: Energy={agent.state.energy:.1f}, Balance={agent.state.balance:.1f}")
            
            # Periodic job injection
            if tick % 5 == 0:
                market.job_board.post_job(Job(
                    id=str(uuid.uuid4()), employer_id="SYSTEM",
                    title="Cleaning Drive", payout=30.0, energy_cost=10.0,
                    location=Position(x=random.randint(0,9), y=random.randint(0,9))
                ))
            
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    run_simulation()