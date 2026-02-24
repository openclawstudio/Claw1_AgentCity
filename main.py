import time
from core.world import World
from core.agent import Agent
from core.economy import EconomyManager

def main():
    print("--- Starting AgentCity MVP ---")
    world = World(width=10, height=10)
    economy = EconomyManager()
    
    # Add agents
    for i in range(5):
        a = Agent(f"agent_{i}", (random.randint(0,9), random.randint(0,9)))
        world.agents.append(a)

    try:
        for i in range(50):
            world.step()
            total_wealth = economy.get_total_wealth(world.agents)
            avg_energy = sum(a.state.energy for a in world.agents) / len(world.agents)
            
            print(f"Tick {i} | Total Wealth: ${total_wealth:.2f} | Avg Energy: {avg_energy:.1f}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    import random
    main()