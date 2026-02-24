import time
import os
from core.world import World
from core.agent import CitizenAgent
from core.models import ResourceType

def run_simulation():
    city = World(width=20, height=20)
    
    # Spawn Citizens with varied traits
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace"]
    for i, name in enumerate(names):
        city.add_agent(CitizenAgent(f"agt-{i}", name, 10, 10))

    print("--- AGENT CITY MVP STARTED ---")
    try:
        while True:
            city.step()
            summary = city.get_summary()
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"CITY DASHBOARD | Tick: {summary['tick']}")
            print(f"Population: {summary['population']} | Tx Count: {summary['total_transactions']}")
            print(f"Average Energy: {summary['avg_energy']}")
            print("Market (Credits):", {k.value: round(v, 2) for k, v in summary['market_prices'].items()})
            print("-" * 40)
            print(f"{'Name':<10} | {'Status':<12} | {'Energy':<6} | {'Credits':<8}")
            for a in city.agents:
                s = a.state
                creds = s.inventory.get(ResourceType.CREDITS, 0)
                print(f"{s.name:<10} | {s.status:<12} | {round(s.energy_level, 1):<6} | {round(creds, 1):<8}")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation halted.")

if __name__ == "__main__":
    run_simulation()