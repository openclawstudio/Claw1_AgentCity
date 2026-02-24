import time
from core.world import AgentCityWorld

def main():
    print("--- Starting AgentCity Simulation ---")
    world = AgentCityWorld(width=15, height=15)
    
    # Setup Infrastructure
    world.add_business("general_store", "grocery", 5, 5)
    
    # Spawn initial citizens
    for i in range(8):
        world.spawn_agent(f"agent_{i}")

    try:
        while True:
            world.update()
            status = world.get_status()
            print(f"Tick: {status['tick']} | Pop: {status['population']} | Treasury: {status['treasury']:.2f}")
            
            if status['tick'] % 5 == 0:
                for a in world.agents[:3]: # Monitor first few agents
                    print(f"  -> {a.id}: Energy {a.state.energy:.1f}, Balance {a.balance:.1f}, Pos ({a.state.pos.x},{a.state.pos.y})")
            
            if status['population'] == 0:
                print("All agents have perished. Simulation over.")
                break

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation ended.")

if __name__ == "__main__":
    main()