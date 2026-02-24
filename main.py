import time
from core.world import World
from core.agent import Citizen

def run_simulation():
    city = World(20, 20)
    
    # Spawn agents
    names = ["Alice", "Bob", "Charlie", "Diana"]
    for name in names:
        agent = Citizen(name, 5, 5)
        city.add_agent(agent)

    print(f"--- Starting AgentCity Simulation ---")
    try:
        for i in range(50):
            state = city.tick()
            print(f"Tick {state.tick}:")
            for a in state.agents:
                dist = city.get_district_at(a.pos.x, a.pos.y)
                print(f"  {a.name} | Energy: {a.energy:.1f} | Credits: {a.wallet:.1f} | Zone: {dist} | Pos: ({a.pos.x},{a.pos.y})")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    run_simulation()