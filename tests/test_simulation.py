import pytest
from core.world import AgentCityWorld
from core.agent import CitizenAgent

def test_agent_movement_bounds():
    world = AgentCityWorld(width=5, height=5)
    agent = CitizenAgent("test", "Tester", world.add_building.__annotations__['building'])
    # Manually set out of bounds
    agent.state.pos.x = 10
    agent.decide(world.economy, [], 5, 5)
    assert agent.state.pos.x <= 5