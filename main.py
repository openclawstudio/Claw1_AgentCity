import time
import random
from core.world import World
from core.agent import CitizenAgent
from core.models import Position, ZoneType
from core.economy import EconomySystem

def run_simulation():
    print("--- Initializing AgentCity MVP v1.1 ---")
    world_width = 10
    world_height = 10
    world = World(world_width, world_height)
    
    # Spawn agents
    agents = [
        CitizenAgent("a1", "Alice", Position(x=0, y=0)),
        CitizenAgent("a2", "Bob", Position(x=5, y=5)),
        CitizenAgent("a3", "Charlie", Position(x=9, y=9))
    ]
    world.agents = [a.state for a in agents]

    ticks = 0
    try:
        while ticks < 100:
            print(f"\n--- Tick {ticks} ---")
            for agent in agents:
                # 1. Decide where to go based on world state
                dx, dy = agent.decide_action(world)
                
                # 2. Apply movement
                agent.apply_move(dx, dy, world_width, world_height)
                
                # 3. Handle Economic/Interaction logic (Industrial zone pays wage)
                current_cell = world.get_cell(agent.state.pos)
                if current_cell.zone == ZoneType.INDUSTRIAL:
                    EconomySystem.pay_wage(agent.state, 5.0)
                    agent.state.last_action = "working"
                
                status = (f"{agent.state.name:7} | "
                          f"Energy: {agent.state.energy:5.1f} | "
                          f"Wallet: {agent.state.wallet:5.1f} | "
                          f"Pos: ({agent.state.pos.x},{agent.state.pos.y}) | "
                          f"Zone: {current_cell.zone.value:11} | "
                          f"Action: {agent.state.last_action}")
                print(status)
            
            # 4. Global world updates (energy decay, etc.)
            world.tick()
            
            ticks += 1
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"\nSimulation crashed: {e}")

if __name__ == "__main__":
    run_simulation()