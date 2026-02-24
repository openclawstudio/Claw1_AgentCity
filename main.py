import time
import random
from core.world import World
from core.agent import CitizenAgent
from core.models import Position

def run_simulation():
    print("--- Initializing AgentCity MVP ---")
    world = World(10, 10)
    
    # Spawn agents
    agents = [
        CitizenAgent("a1", "Alice", Position(x=0, y=0)),
        CitizenAgent("a2", "Bob", Position(x=5, y=5))
    ]
    world.agents = [a.state for a in agents]

    ticks = 0
    try:
        while ticks < 50:
            print(f"\nTick {ticks}")
            for agent in agents:
                action = agent.decide_action({})
                
                # Simple movement implementation
                dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
                agent.move(dx, dy, world.width, world.height)
                
                status = f"{agent.state.name} | Energy: {agent.state.energy:.1f} | Wallet: {agent.state.wallet} | Pos: ({agent.state.pos.x},{agent.state.pos.y}) | Action: {agent.state.last_action}"
                print(status)
            
            world.tick()
            ticks += 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Simulation stopped.")

if __name__ == "__main__":
    run_simulation()