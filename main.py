import time
from core.world import World
from core.agent import CitizenAgent
from core.models import Position, ZoneType
from core.economy import EconomySystem
from core.market import Market, Order

def run_simulation():
    print("--- AgentCity: Autonomous Metropolis v1.2 ---")
    world_width = 10
    world_height = 10
    world = World(world_width, world_height)
    market = Market()
    
    # Spawn agents
    agents = [
        CitizenAgent("a1", "Alice", Position(x=0, y=0)),
        CitizenAgent("a2", "Bob", Position(x=5, y=5)),
        CitizenAgent("a3", "Charlie", Position(x=9, y=9))
    ]
    # Link world agents to the actual state objects
    world.agents = [a.state for a in agents]

    ticks = 0
    try:
        while ticks < 100:
            print(f"\n--- Tick {ticks} ---")
            
            # 1. World-level logic (environment factors)
            world.tick()

            for agent in agents:
                # 2. Agent Decision logic
                dx, dy = agent.decide_action(world)
                
                # 3. Apply movement
                agent.apply_move(dx, dy, world_width, world_height)
                
                # 4. Interact with the environment based on new position
                current_cell = world.get_cell(agent.state.pos)
                
                if current_cell.zone == ZoneType.INDUSTRIAL:
                    # Working provides currency but drains energy (processed in world.tick + here)
                    EconomySystem.pay_wage(agent.state, 10.0)
                    agent.state.last_action = "working"
                
                elif current_cell.zone == ZoneType.COMMERCIAL:
                    # Try to buy 'rations' if wealthy
                    if agent.state.wallet > 40:
                        agent.state.last_action = "browsing_market"
                        # Simulation of market interaction: Post an order if hungry
                        if agent.state.energy < 50:
                            match = market.find_match("energy_pack", 20.0)
                            if match:
                                # Logic for transaction would go here
                                agent.state.last_action = "buying_resource"
                
                status = (f"{agent.state.name:7} | "
                          f"Energy: {agent.state.energy:5.1f} | "
                          f"Wallet: {agent.state.wallet:5.1f} | "
                          f"Pos: ({agent.state.pos.x},{agent.state.pos.y}) | "
                          f"Zone: {current_cell.zone.value:11} | "
                          f"Action: {agent.state.last_action}")
                print(status)
            
            ticks += 1
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"\nSimulation crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_simulation()