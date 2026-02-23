import pytest
from core.world import World
from core.models import AgentState, Vector2D, SimulationConfig
from core.agent import CitizenAgent

@pytest.mark.asyncio
async def test_agent_movement():
    config = SimulationConfig(width=10, height=10)
    world = World(config)
    state = AgentState(id="test", name="test", position=Vector2D(x=0, y=0))
    agent = CitizenAgent(state)
    # Move towards (5,5) should increment x and y by 1
    agent.move_towards(Vector2D(x=5, y=5), world)
    assert state.position.x == 1
    assert state.position.y == 1

@pytest.mark.asyncio
async def test_economic_transaction():
    world = World()
    s1 = AgentState(id="a1", name="a1", position=Vector2D(x=0,y=0))
    s2 = AgentState(id="a2", name="a2", position=Vector2D(x=0,y=0))
    s1.economy.balance = 50
    world.add_agent(s1)
    world.add_agent(s2)
    
    success = await world.process_transaction("a1", "a2", 20.0, "food")
    assert success is True
    assert world.agents["a1"].economy.balance == 30
    assert world.agents["a2"].economy.balance == 20