import pytest
from core.world import World
from core.agent import Citizen
from core.models import Position

@pytest.mark.asyncio
async def test_agent_movement():
    world = World(width=10, height=10)
    citizen = Citizen(name="Tester", position=Position(x=5, y=5))
    world.add_entity(citizen)
    
    initial_pos = (citizen.position.x, citizen.position.y)
    await citizen.update(world)
    new_pos = (citizen.position.x, citizen.position.y)
    
    # Check that energy decreased
    assert citizen.energy < 100.0
    # Check position stays within bounds
    assert 0 <= citizen.position.x < 10
    assert 0 <= citizen.position.y < 10