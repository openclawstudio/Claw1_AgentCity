import unittest
from core.world import World
from core.agent import Citizen
from core.models import Position, Job, ZoneType
from core.market import Market
from core.economy import EconomyManager

class TestAgentCity(unittest.TestCase):
    def test_agent_movement_fixed(self):
        world = World(5, 5)
        # Set center pos
        agent = Citizen("Tester", Position(x=2, y=2))
        initial_pos = (agent.state.pos.x, agent.state.pos.y)
        agent.move_randomly(world)
        new_pos = (agent.state.pos.x, agent.state.pos.y)
        # Since (0,0) is removed from moves, it MUST change position
        self.assertNotEqual(initial_pos, new_pos)

    def test_economy_transaction(self):
        world = World(10, 10)
        economy = EconomyManager()
        agent = Citizen("Worker", Position(x=0, y=0))
        job = Job(id="1", employer_id="SYS", title="Task", payout=10.0, energy_cost=5.0, location=Position(x=1,y=1))
        agent.work(job, economy, world)
        self.assertEqual(agent.balance, 10.0)
        self.assertEqual(economy.global_gdp, 10.0)
        self.assertEqual(len(economy.ledger.transactions), 1)
        self.assertEqual(agent.state.pos.x, 1)

    def test_zoning_initialization(self):
        world = World(12, 12)
        self.assertEqual(world.grid[0][0].zone, ZoneType.RESIDENTIAL)
        self.assertEqual(world.grid[5][0].zone, ZoneType.COMMERCIAL)
        self.assertEqual(world.grid[10][0].zone, ZoneType.INDUSTRIAL)

if __name__ == '__main__':
    unittest.main()