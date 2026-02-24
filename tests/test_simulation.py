import pytest
from core.world import World
from core.agent import CitizenAgent
from core.models import ResourceType

def test_agent_energy_consumption():
    world = World(10, 10)
    agent = CitizenAgent("test-1", "Test", 5, 5)
    initial_energy = agent.state.energy_level
    agent.step(world)
    assert agent.state.energy_level < initial_energy

def test_market_price_evolution():
    world = World(10, 10)
    initial_price = world.market.get_price(ResourceType.ENERGY)
    # Simulate high demand
    for _ in range(5):
        world.market.transaction_event(ResourceType.ENERGY, is_buy=True)
    world.market.update_prices()
    assert world.market.get_price(ResourceType.ENERGY) > initial_price

def test_economy_ledger():
    world = World(10, 10)
    agent = CitizenAgent("test-1", "Test", 5, 5)
    agent.state.inventory[ResourceType.CREDITS] = 1000
    agent.seek_energy(world)
    assert len(world.economy.ledger.transactions) > 0
    assert world.economy.ledger.transactions[0]['amount'] == 1