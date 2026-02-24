import time
import random
from core.world import World
from core.agent import Citizen

def run_simulation(ticks=50):
    width, height = 20, 20
    city = World(width, height)
    
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
    for name in names:
        start_x = random.randint(0, width - 1)
        start_y = random.randint(0, height - 1)
        agent = Citizen(name, start_x, start_y)
        city.add_agent(agent)

    print(f"\033[94m--- AgentCity Metropolis Simulation Starting ---\033[0m")
    try:
        for i in range(ticks):
            state = city.tick()
            
            print(f"\nTick {state.tick} | Total Transactions: {len(city.economy.transactions)}")
            print("-" * 80)
            for a in state.agents:
                dist = city.get_district_at(a.pos.x, a.pos.y)
                goal = a.current_goal or "IDLE"
                print(f"{a.name:8} | E: {a.energy:5.1f} | $: {a.wallet:7.1f} | Zone: {dist:12} | Goal: {goal}")
            
            time.sleep(0.1)
            
        print(f"\n\033[92mSimulation Complete. Total Economic Activity: {len(city.economy.transactions)} trades.\033[0m")
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    run_simulation()