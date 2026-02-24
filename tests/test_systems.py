import pytest
from core.models import AgentState, Position
from core.economy import EconomySystem
from core.market import Market, Order

def test_transaction_success():
    buyer = AgentState(id="a1", name="Buyer", pos=Position(x=0,y=0), wallet=100.0)
    seller = AgentState(id="a2", name="Seller", pos=Position(x=0,y=0), wallet=0.0, inventory={"bread": 5})
    
    success = EconomySystem.process_transaction(buyer, seller, "bread", 20.0)
    
    assert success is True
    assert buyer.wallet == 80.0
    assert seller.wallet == 19.0 # 20 - 5% tax
    assert buyer.inventory["bread"] == 1
    assert seller.inventory["bread"] == 4

def test_market_matching():
    market = Market()
    market.post_order(Order(agent_id="s1", item="fuel", price=10.0, order_type="sell"))
    market.post_order(Order(agent_id="s2", item="fuel", price=5.0, order_type="sell"))
    
    match = market.find_match("fuel", 15.0)
    assert match is not None
    assert match.price == 5.0
    assert match.agent_id == "s2"