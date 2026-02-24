import time
import os
from core.world import World

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Initializing Claw1 AgentCity...")
    city = World(30, 30)
    
    # Seed initial population
    for _ in range(15):
        city.spawn_agent()

    try:
        while True:
            city.tick()
            
            # Simple CLI Dashboard
            if city.tick_counter % 2 == 0:
                # clear_screen()
                avg_energy = sum(a.state.energy for a in city.agents.values()) / max(1, len(city.agents))
                total_wealth = sum(a.state.balance for a in city.agents.values()) + sum(b.vault for b in city.businesses.values())
                
                print(f"--- AgentCity Stats [Tick {city.tick_counter}] ---")
                print(f"Population: {len(city.agents):<4} | Businesses: {len(city.businesses):<4}")
                print(f"Avg Energy: {avg_energy:<4.1f} | Total GDP: {total_wealth:<6.2f}")
                print("-" * 40)
            
            if len(city.agents) == 0:
                print("The city has become a ghost town. Simulation ended.")
                break
                
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCity simulation paused. Saving state...")

if __name__ == '__main__':
    main()