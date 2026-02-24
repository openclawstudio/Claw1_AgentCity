import unittest
from core.world import World
from core.agent import Citizen

class TestSimulation(unittest.TestCase):
    def test_world_init(self):
        world = World(10, 10)
        self.assertEqual(len(world.state.districts), 2)

    def test_agent_movement(self):
        world = World(10, 10)
        agent = Citizen("Tester", 5, 5)
        world.add_agent(agent)
        original_pos = (agent.state.pos.x, agent.state.pos.y)
        agent.wander(world)
        new_pos = (agent.state.pos.x, agent.state.pos.y)
        self.assertNotEqual(original_pos, new_pos)

    def test_economy_transaction(self):
        world = World(10, 10)
        world.economy.record_transaction("A", "B", 10.0, "CREDITS", 1)
        self.assertEqual(len(world.economy.transactions), 1)
        self.assertEqual(world.economy.transactions[0].amount, 10.0)

if __name__ == '__main__':
    unittest.main()