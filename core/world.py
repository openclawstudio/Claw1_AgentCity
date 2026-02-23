import asyncio
import logging
from typing import Dict, List
from core.models import AgentState, Vector2D, Transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorldEngine")

class Ledger:
    def __init__(self):
        self.history: List[Transaction] = []

    def record(self, transaction: Transaction):
        self.history.append(transaction)
        logger.info(f"[TX] {transaction.sender_id} -> {transaction.receiver_id}: ${transaction.amount}")

class World:
    def __init__(self, width: int = 50, height: int = 50):
        self.width = width
        self.height = height
        self.tick_counter = 0
        self.agents: Dict[str, AgentState] = {}
        self.ledger = Ledger()
        # Zoning: (x_range, y_range) -> ZoneType
        self.zones = {
            "park": {"x": range(0, 10), "y": range(0, 10), "bonus": "energy_regen"},
            "market": {"x": range(20, 30), "y": range(20, 30), "bonus": "trade_hub"}
        }

    def add_agent(self, agent_state: AgentState):
        self.agents[agent_state.id] = agent_state

    def get_zone(self, pos: Vector2D):
        for zone_name, data in self.zones.items():
            if pos.x in data['x'] and pos.y in data['y']:
                return zone_name
        return "suburbs"

    async def tick(self):
        self.tick_counter += 1
        for agent_id, state in self.agents.items():
            # Apply Zone Effects
            zone = self.get_zone(state.position)
            if zone == "park":
                state.energy = min(100, state.energy + 2)
            
            # Passive Energy Drain
            state.energy -= 0.5
            
            if state.energy < 10:
                logger.warning(f"Agent {agent_id} is exhausted!")