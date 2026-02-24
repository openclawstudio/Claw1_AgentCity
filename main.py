import time
from core.world import CityWorld

def main():
    print("🏙️ AgentCity MVP Starting...")
    world = CityWorld(width=10, height=10)
    
    # Spawn initial population
    for _ in range(5):
        world.spawn_agent()
    
    try:
        while True:
            stats = world.tick()
            print(f"Tick {stats['tick']} | Pop: {stats['population']} | Trade Volume: {stats['transactions']}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCity simulation paused.")

if __name__ == "__main__":
    main()