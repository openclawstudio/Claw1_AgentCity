import time
from core.world import AgentCityWorld

def main():
    print("--- Starting AgentCity Simulation ---")
    world = AgentCityWorld(width=10, height=10)
    
    # Spawn initial citizens
    for i in range(5):
        world.spawn_agent(f"agent_{i}")

    try:
        while True:
            world.update()
            status = world.get_status()
            print(f"Tick: {status['tick']} | Pop: {status['population']} | Treasury: {status['treasury']:.2f}")
            
            if status['tick'] % 10 == 0:
                for a in world.agents:
                    print(f"  -> {a.id}: Energy {a.state.energy:.1f}, Balance {a.balance:.1f}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation ended.")

if __name__ == "__main__":
    main()