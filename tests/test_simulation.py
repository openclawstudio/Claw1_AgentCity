from core.world import World
from core.models import Role

def test_agent_spawning():
    world = World(10, 10)
    world.spawn_agent()
    assert len(world.agents) == 1

def test_agent_energy_depletion():
    world = World(10, 10)
    agent = world.spawn_agent()
    initial_energy = agent.state.energy
    world.tick()
    assert agent.state.energy < initial_energy

def test_entrepreneurship():
    world = World(10, 10)
    agent = world.spawn_agent()
    agent.state.balance = 2000
    world.tick()
    assert agent.state.role == Role.ENTREPRENEUR
    assert len(world.businesses) > 0