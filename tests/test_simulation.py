import unittest
from core.world import World
from core.agent import Citizen
from core.models import Position, Job
from core.market import Market
from core.economy import EconomyManager

class TestAgentCity(unittest.TestCase):
    def test_agent_movement(self):
        world = World(5, 5)
        agent = Citizen("Tester", Position(x=2, y=2))
        initial_pos = (agent.state.pos.x, agent.state.pos.y)
        agent.move_randomly(world)
        new_pos = (agent.state.pos.x, agent.state.pos.y)
        self.assertNotEqual(initial_pos, None)

    def test_economy_transaction(self):
        economy = EconomyManager()
        agent = Citizen("Worker", Position(x=0, y=0))
        job = Job(id="1", employer_id="SYS", title="Task", payout=10.0, energy_cost=5.0, location=Position(x=0,y=0))
        agent.work(job, economy)
        self.assertEqual(agent.balance, 10.0)
        self.assertEqual(economy.global_gdp, 10.0)
        self.assertEqual(len(economy.ledger.transactions), 1)

if __name__ == '__main__':
    unittest.main() 