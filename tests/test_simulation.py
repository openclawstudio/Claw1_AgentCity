import pytest
from core.world import CityWorld
from core.models import ResourceType, OrderType, MarketOrder
import uuid

def test_market_matching():
    world = CityWorld()
    # Place a sell order
    sell = MarketOrder(id="1", agent_id="a1", resource=ResourceType.ENERGY, order_type=OrderType.SELL, quantity=10, price=10.0, timestamp=0)
    # Place a buy order at higher price
    buy = MarketOrder(id="2", agent_id="a2", resource=ResourceType.ENERGY, order_type=OrderType.BUY, quantity=10, price=12.0, timestamp=0)
    
    world.market.place_order(sell)
    world.market.place_order(buy)
    
    assert len(world.market.transaction_history) == 1
    assert world.market.transaction_history[0]['price'] == 10.0

def test_agent_lifecycle():
    world = CityWorld()
    world.spawn_agent()
    agent_id = list(world.agents.keys())[0]
    agent = world.agents[agent_id]
    
    initial_energy = agent.state.energy
    world.tick()
    # Energy should decrease or change based on logic
    assert agent.state.energy != initial_energy