import time
import os
from core.world import World
from core.agent import Citizen

def run_simulation(ticks=50):
    city = World(20, 20)
    
    # Spawn agents with diverse positions
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    for i, name in enumerate(names):
        agent = Citizen(name, random_pos := (i % 20), (i * 3) % 20)
        city.add_agent(agent)

    print(f"\033[94m--- AgentCity Metropolis Simulation Starting ---\033[0m")
    try:
        for i in range(ticks):
            state = city.tick()
            # Clear screen for a pseudo-UI effect
            # os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\nTick {state.tick} | Total Transactions: {len(city.economy.transactions)}")
            print("-" * 60)
            for a in state.agents:
                dist = city.get_district_at(a.pos.x, a.pos.y)
                goal = a.current_goal or "IDLE"
                print(f"{a.name:8} | E: {a.energy:5.1f} | $: {a.wallet:6.1f} | Zone: {dist:12} | Goal: {goal}")
            time.sleep(0.1)
            
        print(f"\n\033[92mSimulation Complete. Final Economic Activity: {len(city.economy.transactions)} trades.\033[0m")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    run_simulation()
