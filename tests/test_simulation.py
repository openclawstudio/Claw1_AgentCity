import unittest
from core.world import World
from core.agent import Agent
from core.models import ZoneType

class TestAgentCity(unittest.TestCase):
    def test_world_init(self):
        world = World(5, 5)
        self.assertEqual(len(world.zones), 25)

    def test_agent_energy_death(self):
        world = World(5, 5)
        agent = Agent("test", (0,0))
        agent.state.energy = 0.1
        world.agents.append(agent)
        world.step()
        self.assertFalse(agent.alive)
        self.assertEqual(len(world.agents), 0)

    def test_economy_transfer(self):
        world = World(5, 5)
        a1 = Agent("a1", (0,0))
        a2 = Agent("a2", (0,0))
        a1.state.wallet = 100
        a2.state.wallet = 0
        success = world.economy.transfer(a1, a2, 50, "test", 1)
        self.assertTrue(success)
        self.assertEqual(a1.state.wallet, 50)
        self.assertEqual(a2.state.wallet, 50)

if __name__ == '__main__':
    unittest.main()