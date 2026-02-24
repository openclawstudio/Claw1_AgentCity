import time
import os
import random
from core.world import World
from core.agent import Citizen

def run_simulation(ticks=50):
    # Seed for reproducibility during testing if needed
    # random.seed(42)
    
    city = World(20, 20)
    
    # Spawn agents with diverse positions
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
    for i, name in enumerate(names):
        # Ensure agents start within bounds
        start_x = random.randint(0, 19)
        start_y = random.randint(0, 19)
        agent = Citizen(name, start_x, start_y)
        city.add_agent(agent)

    print(f"\033[94m--- AgentCity Metropolis Simulation Starting ---\033[0m")
    try:
        for i in range(ticks):
            state = city.tick()
            
            # Optional: Clear screen for a pseudo-UI effect
            # os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\nTick {state.tick} | Total Transactions: {len(city.economy.transactions)}")
            print("-" * 70)
            for a in state.agents:
                dist = city.get_district_at(a.pos.x, a.pos.y)
                goal = a.current_goal or "IDLE"
                print(f"{a.name:8} | E: {a.energy:5.1f} | $: {a.wallet:7.1f} | Zone: {dist:12} | Goal: {goal}")
            
            # Moderate speed for readability
            time.sleep(0.2)
            
        print(f"\n\033[92mSimulation Complete. Total Economic Activity: {len(city.economy.transactions)} trades.\033[0m")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == \"__main__\":
    run_simulation()