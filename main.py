import time
import random
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
    
    # Setup initial state for a 'Merchant'
    agents[1].state.inventory["energy_pack"] = 10
    market.post_order(Order(agent_id="a2", item="energy_pack", price=15.0, order_type="sell"))

    world.agents = [a.state for a in agents]

    ticks = 0
    try:
        while ticks < 100:
            print(f"\n--- Tick {ticks} ---")
            world.tick()

            for agent in agents:
                if agent.state.energy <= 0:
                    print(f"{agent.state.name:7} | EXHAUSTED (Incapacitated)")
                    continue

                # 1. Decision logic
                dx, dy = agent.decide_action(world)
                agent.apply_move(dx, dy, world_width, world_height)
                
                current_cell = world.get_cell(agent.state.pos)
                
                # 2. Zone-based interactions
                if current_cell.zone == ZoneType.INDUSTRIAL:
                    EconomySystem.pay_wage(agent.state, 12.0)
                    agent.state.last_action = "working"
                
                elif current_cell.zone == ZoneType.COMMERCIAL:
                    # Try to maintain survival
                    if agent.state.energy < 40 and agent.state.wallet >= 15:
                        match = market.find_match("energy_pack", agent.state.wallet)
                        if match:
                            # Find the seller agent
                            seller_agent = next((a for a in agents if a.state.id == match.agent_id), None)
                            if seller_agent:
                                success = EconomySystem.process_transaction(
                                    agent.state, seller_agent.state, "energy_pack", match.price
                                )
                                if success:
                                    EconomySystem.consume_resource(agent.state, "energy_pack", 30.0)
                                    agent.state.last_action = "bought_and_consumed"
                                    # If seller is out of stock, remove listing
                                    if seller_agent.state.inventory.get("energy_pack", 0) <= 0:
                                        market.remove_order(match.id)

                status = (f"{agent.state.name:7} | "
                          f"Energy: {agent.state.energy:5.1f} | "
                          f"Wallet: {agent.state.wallet:5.1f} | "
                          f"Pos: ({agent.state.pos.x},{agent.state.pos.y}) | "
                          f"Zone: {current_cell.zone.value:11} | "
                          f"Action: {agent.state.last_action}")
                print(status)
            
            ticks += 1
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"\nSimulation crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_simulation()