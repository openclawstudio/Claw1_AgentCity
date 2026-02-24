import time
import random
from core.world import World
from core.agent import Agent

def main():
    print("--- Starting AgentCity Simulation ---")
    width, height = 10, 10
    world = World(width=width, height=height)
    
    roles = ["worker", "merchant", "builder", "citizen", "producer"]
    for i in range(15):
        pos = (random.randint(0, width-1), random.randint(0, height-1))
        role = roles[i % len(roles)]
        a = Agent(f"agent_{i}", pos, job_role=role)
        world.agents.append(a)

    print(f"Created {len(world.agents)} agents in a {width}x{height} world.")

    try:
        for i in range(100):
            world.step()
            
            alive_agents = [a for a in world.agents if a.alive]
            if not alive_agents:
                print(f"Tick {i:03d} | All agents have perished.")
                break

            total_wealth = sum(a.state.wallet for a in alive_agents)
            avg_energy = sum(a.state.energy for a in alive_agents) / len(alive_agents)
            active_offers = len(world.market.offers)
            
            if i % 10 == 0:
                print(f"Tick {i:03d} | Population: {len(alive_agents)} | Wealth: ${total_wealth:7.2f} | Avg Energy: {avg_energy:5.1f} | Market Offers: {active_offers}")
            
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    
    print("--- Final Stats ---")
    print(f"Total Ticks: {world.tick_count}")
    alive_final = [a for a in world.agents if a.alive]
    print(f"Surviving Agents: {len(alive_final)}")
    print(f"Total Economic Wealth: ${sum(a.state.wallet for a in alive_final):.2f}")

if __name__ == "__main__":
    main()