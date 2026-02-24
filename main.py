import time
from core.world import World
from core.agent import Citizen
from core.market import Market
from core.economy import EconomyManager
from core.models import Position, Job
import uuid

def run_simulation():
    print("--- Starting AgentCity MVP ---")
    world = World(10, 10)
    market = Market()
    economy = EconomyManager()
    
    # Spawn agents
    citizens = [
        Citizen(f"Agent_{i}", Position(x=random.randint(0,9), y=random.randint(0,9)))
        for i in range(5)
    ]

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
            print(f"\nTick {tick} | GDP: {economy.global_gdp}")
            for agent in citizens:
                agent.step(market, economy, world)
                print(f"{agent.state.name}: Energy={agent.state.energy}, Balance={agent.state.balance}")
            
            # Periodic job injection
            if tick % 5 == 0:
                market.job_board.post_job(Job(
                    id=str(uuid.uuid4()), employer_id="SYSTEM",
                    title="Cleaning Drive", payout=30.0, energy_cost=10.0,
                    location=Position(x=random.randint(0,9), y=random.randint(0,9))
                ))
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Simulation stopped.")

import random
if __name__ == "__main__":
    run_simulation()