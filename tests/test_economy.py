import pytest
from core.economy import Economy
from core.models import Position, ResourceType
from core.agent import Citizen

class MockEntity:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance

def test_transfer_success():
    economy = Economy()
    alice = MockEntity("alice", 100.0)
    bob = MockEntity("bob", 0.0)
    
    success = economy.transfer(alice, bob, 50.0, ResourceType.CREDITS, 1)
    
    assert success is True
    assert alice.balance == 50.0
    assert bob.balance == 47.5 # 50 - 5% tax
    assert economy.treasury == 2.5
    assert len(economy.transaction_history) == 1