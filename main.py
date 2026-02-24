import time
from core.world import World

def main():
    print("Initializing Claw1 AgentCity...")
    city = World(30, 30)
    
    # Seed initial population
    for _ in range(10):
        city.spawn_agent()

    try:
        while True:
            city.tick()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCity simulation paused.")

if __name__ == "__main__":
    main()