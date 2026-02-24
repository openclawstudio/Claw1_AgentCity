import time
import os
from core.world import AgentCityWorld
from core.agent import CitizenAgent
from core.entity import Building, BuildingType
from core.models import Position

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_simulation():
    world = AgentCityWorld(30, 30)
    
    # Setup City Infrastructure
    world.add_building(Building("h1", BuildingType.HOME, Position(x=2, y=2)))
    world.add_building(Building("o1", BuildingType.OFFICE, Position(x=15, y=15)))
    world.add_building(Building("m1", BuildingType.MARKET, Position(x=5, y=10)))

    # Spawn Citizens
    citizens = [
        CitizenAgent("a1", "Alice", Position(x=0, y=0)),
        CitizenAgent("a2", "Bob", Position(x=10, y=10))
    ]
    for c in citizens: world.add_agent(c)

    print("Starting AgentCity MVP...")
    try:
        for i in range(100):
            world.step()
            clear_screen()
            stats = world.get_status()
            print(f"--- AgentCity Tick {stats['tick']} ---")
            for a in world.agents:
                print(f"{a.state.name}: Pos({a.state.pos.x},{a.state.pos.y}) | Goal: {a.state.current_goal} | Energy: {a.state.energy:.1f} | Wealth: ${a.state.wealth}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation Stopped.")

if __name__ == "__main__":
    run_simulation()