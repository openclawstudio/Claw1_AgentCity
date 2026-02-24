from core.world import World
from core.agent import Citizen
from core.models import ZoneType

def test_simulation_step():
    city = World(10, 10)
    alice = Citizen("Alice", 0, 0)
    city.add_agent(alice)
    initial_energy = alice.state.energy
    city.step()
    assert alice.state.energy != initial_energy

def test_economic_transaction():
    city = World(5, 5)
    # Force a citizen into industrial zone
    worker = Citizen("Worker", 0, 0)
    city.grid[(0, 0)] = ZoneType.INDUSTRIAL
    city.add_agent(worker)
    city.step()
    assert worker.state.wallet.balance > 0
    assert len(city.ledger) > 0