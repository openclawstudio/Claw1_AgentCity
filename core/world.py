import asyncio
import logging
from typing import Dict, List, Optional
from core.models import AgentState, Vector2D, Transaction, EntityType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorldEngine")

class Ledger:
    def __init__(self):
        self.history: List[Transaction] = []

    def record(self, transaction: Transaction):
        self.history.append(transaction)
        logger.info(f"[TX] {transaction.sender_id} -> {transaction.receiver_id}: ${transaction.amount} ({transaction.item or 'Service'})")

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

    def get_zone(self, pos: Vector2D) -> str:
        for zone_name, data in self.zones.items():
            if pos.x in data['x'] and pos.y in data['y']:
                return zone_name
        return "suburbs"

    def get_entities_at(self, pos: Vector2D, exclude_id: Optional[str] = None) -> List[AgentState]:
        return [a for a in self.agents.values() if a.position.x == pos.x and a.position.y == pos.y and a.id != exclude_id]

    async def process_transaction(self, sender_id: str, receiver_id: str, amount: float, item: str = None) -> bool:
        sender = self.agents.get(sender_id)
        receiver = self.agents.get(receiver_id)
        
        if sender and receiver and sender.economy.balance >= amount:
            sender.economy.balance -= amount
            receiver.economy.balance += amount
            tx = Transaction(
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                item=item,
                timestamp=self.tick_counter
            )
            self.ledger.record(tx)
            return True
        return False

    async def tick(self):
        self.tick_counter += 1
        for agent_id, state in self.agents.items():
            # Apply Zone Effects
            zone = self.get_zone(state.position)
            if zone == "park":
                state.energy = min(100.0, state.energy + 2.0)
            
            # Passive Energy Drain
            state.energy -= 0.5
            
            if state.energy <= 0:
                state.energy = 0
                logger.warning(f"Agent {agent_id} is incapacitated!")