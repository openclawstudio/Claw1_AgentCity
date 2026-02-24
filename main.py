import time
import os
from core.world import World
from core.agent import Citizen

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    city = World(20, 20)
    
    # Populate City
    citizens = [
        Citizen("Alice", 0, 0),
        Citizen("Bob", 5, 5),
        Citizen("Charlie", 10, 10)
    ]
    for c in citizens:
        city.add_agent(c)

    print("Starting AgentCity simulation...")
    try:
        while True:
            city.step()
            
            # Dashboard
            clear_screen()
            print(f"--- AgentCity Metrics (Tick: {city.tick_counter}) ---")
            total_gdp = sum(c.state.wallet.balance for c in city.agents.values())
            avg_energy = sum(c.state.energy for c in city.agents.values()) / len(city.agents)
            
            print(f"Population: {len(city.agents)} | Total GDP: {total_gdp:.2f} | Avg Energy: {avg_energy:.1f}")
            print("\nCitizen Status:")
            for c in city.agents.values():
                zone = city.get_zone(c.pos)
                print(f"- {c.name}: Pos({c.pos.x}, {c.pos.y}) | Energy: {c.state.energy:.1f} | Wallet: {c.state.wallet.balance:.2f} | Zone: {zone.name}")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation paused. City state saved.")

if __name__ == "__main__":
    main()