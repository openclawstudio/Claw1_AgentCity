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
        world.get_cell(agent.state.pos).agents.append(agent.id)
        initial_pos = (agent.state.pos.x, agent.state.pos.y)
        agent.move_randomly(world)
        new_pos = (agent.state.pos.x, agent.state.pos.y)
        # While random move could land on same cell if clamped at edges,
        # in a 5x5 at (2,2) it must move.
        self.assertNotEqual(initial_pos, (agent.state.pos.x, agent.state.pos.y))

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

if __name__ == '__main__':
    unittest.main()