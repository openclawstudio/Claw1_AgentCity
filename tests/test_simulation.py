import pytest
from core.world import World
from core.agent import Citizen
from core.models import ZoneType, Position

def test_simulation_step():
    city = World(10, 10)
    alice = Citizen("Alice", 0, 0)
    city.add_agent(alice)
    initial_energy = alice.state.energy
    city.step()
    # Energy should decay or change after a step
    assert alice.state.energy < initial_energy or alice.state.energy > initial_energy

def test_economic_transaction():
    city = World(5, 5)
    # Force worker into an industrial zone for immediate work
    worker = Citizen("Worker", 0, 0)
    city.grid[(0, 0)] = ZoneType.INDUSTRIAL
    # Update cache since we manually updated the grid
    city._zone_cache[ZoneType.INDUSTRIAL].append((0, 0))
    city.add_agent(worker)
    
    # First step might move or stay, but since it's at 0,0 and target is 0,0, it works
    city.step()
    assert worker.state.wallet.balance > 0
    assert len(city.ledger) > 0

def test_agent_movement():
    city = World(10, 10)
    city.grid[(5, 5)] = ZoneType.RESIDENTIAL
    city._zone_cache[ZoneType.RESIDENTIAL] = [(5, 5)]
    
    agent = Citizen("Traveler", 0, 0)
    # Force rest intention to trigger movement to (5,5)
    agent.state.energy = 10.0
    
    # It should take several steps to reach (5,5) from (0,0)
    city.add_agent(agent)
    city.step()
    
    assert agent.pos.x > 0 or agent.pos.y > 0
    assert agent.pos.x <= 5 and agent.pos.y <= 5