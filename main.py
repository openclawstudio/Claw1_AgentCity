import time
import os
from core.world import World
from core.agent import CitizenAgent

def run_simulation():
    # Init City
    city = World(width=20, height=20)
    
    # Spawn Citizens
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    for i, name in enumerate(names):
        city.add_agent(CitizenAgent(f"agt-{i}", name, 10, 10))

    print("--- AGENT CITY MVP STARTED ---")
    try:
        while True:
            city.step()
            summary = city.get_summary()
            
            # Clear screen for dashboard effect
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"City Heartbeat - Tick: {summary['tick']}")
            print(f"Population: {summary['population']}")
            print(f"Average Energy: {summary['avg_energy']}")
            print("Market Prices (Credits):", {k.value: round(v, 2) for k, v in summary['market_prices'].items()})
            print("\nCitizen Status:")
            for a in city.agents:
                print(f" - {a.state.name}: {a.state.status} | Energy: {round(a.state.energy_level, 1)} | Credits: {round(a.state.inventory.get('credits', 0), 1)}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation halted by user.")

if __name__ == "__main__":
    run_simulation()
