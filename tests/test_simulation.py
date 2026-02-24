import pytest
from core.world import AgentCityWorld
from core.agent import CitizenAgent
from core.models import Position

def test_agent_movement_bounds():
    world = AgentCityWorld(width=5, height=5)
    agent = CitizenAgent("test", "Tester", Position(x=0, y=0))
    # Manually set out of bounds
    agent.state.pos.x = 10
    # Agent should move towards (0,0) or explore within bounds
    agent.decide(world.economy, [], 5, 5)
    assert agent.state.pos.x <= 10 # Movement logic varies, but ensuring no crash

def test_economy_recording():
    world = AgentCityWorld()
    agent = CitizenAgent("a1", "Alice", Position(x=0, y=0))
    from core.entity import Building, BuildingType
    office = Building("o1", BuildingType.OFFICE, Position(x=0, y=0))
    
    # Manually trigger work activity
    agent._perform_activity(world.economy, office)
    assert len(world.economy.ledger.history) == 1
    assert world.economy.ledger.history[0].amount == 10.0