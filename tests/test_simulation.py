import unittest
from core.world import World
from core.agent import Citizen

class TestSimulation(unittest.TestCase):
    def test_world_init(self):
        world = World(10, 10)
        self.assertEqual(len(world.state.districts), 2)

    def test_agent_movement(self):
        world = World(10, 10)
        # Edge case: Put agent in middle so move is likely to succeed
        agent = Citizen("Tester", 5, 5)
        world.add_agent(agent)
        original_pos = (agent.state.pos.x, agent.state.pos.y)
        
        # Force movement by trying multiple times if random fails
        moved = False
        for _ in range(10):
            agent.wander(world)
            if (agent.state.pos.x, agent.state.pos.y) != original_pos:
                moved = True
                break
        self.assertTrue(moved)

    def test_economy_transaction(self):
        world = World(10, 10)
        world.economy.record_transaction("A", "B", 10.0, "CREDITS", 1)
        self.assertEqual(len(world.economy.transactions), 1)
        self.assertEqual(world.economy.transactions[0].amount, 10.0)

if __name__ == '__main__':
    unittest.main()