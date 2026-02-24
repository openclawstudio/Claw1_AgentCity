import pytest
from core.world import AgentCityWorld
from core.agent import CitizenAgent
from core.models import Position
from core.entity import Building, BuildingType

def test_agent_movement_logic():
    world = AgentCityWorld(width=10, height=10)
    agent = CitizenAgent("test", "Tester", Position(x=0, y=0))
    target_pos = Position(x=5, y=5)
    # Test manual move towards
    agent._move_towards(target_pos)
    assert agent.state.pos.x == 1 or agent.state.pos.y == 1
    assert agent.state.energy < 100.0

def test_economy_recording():
    world = AgentCityWorld()
    agent = CitizenAgent("a1", "Alice", Position(x=0, y=0))
    office = Building("o1", BuildingType.OFFICE, Position(x=0, y=0))
    
    # Manually trigger work activity
    agent._perform_activity(world.economy, office)
    assert len(world.economy.ledger.history) == 1
    assert world.economy.ledger.history[0].amount == 15.0
    assert agent.state.wealth == 65.0 # 50 (default) + 15

def test_full_decision_loop():
    world = AgentCityWorld(width=10, height=10)
    world.add_building(Building("h1", BuildingType.HOME, Position(x=1, y=1)))
    agent = CitizenAgent("a1", "Alice", Position(x=1, y=1))
    agent.state.energy = 10.0 # Force rest
    
    world.add_agent(agent)
    world.step()
    
    assert agent.state.current_goal == "rest"
    assert agent.state.energy > 10.0