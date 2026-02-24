import pytest
from core.world import AgentCityWorld

def test_simulation_tick_depletes_energy():
    world = AgentCityWorld(10, 10)
    world.spawn_agent("test_agent")
    initial_energy = world.agents[0].state.energy
    world.update()
    assert world.agents[0].state.energy < initial_energy

def test_agent_buys_food():
    world = AgentCityWorld(10, 10)
    world.add_business("store", "grocery", 1, 1)
    world.spawn_agent("hungry_agent")
    agent = world.agents[0]
    agent.state.pos.x, agent.state.pos.y = 1, 1
    agent.state.energy = 20
    agent.balance = 50
    
    world.update()
    
    assert agent.state.energy > 20
    assert agent.balance < 50