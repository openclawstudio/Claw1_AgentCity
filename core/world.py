import asyncio
import logging
from typing import Dict, List, Optional
from core.models import AgentState, Vector2D, Transaction, EntityType

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
        self.events: List[dict] = []  # Simple event bus for localized interactions
        self.zones = {
            "park": {"x": range(0, 11), "y": range(0, 11), "bonus": "energy_regen"},
            "market": {"x": range(20, 31), "y": range(20, 31), "bonus": "trade_hub"}
        }

    def add_agent(self, agent_state: AgentState):
        self.agents[agent_state.id] = agent_state

    def get_zone(self, pos: Vector2D) -> str:
        for zone_name, data in self.zones.items():
            if pos.x in data['x'] and pos.y in data['y']:
                return zone_name
        return "suburbs"

    def emit_event(self, event_type: str, data: dict):
        self.events.append({"tick": self.tick_counter, "type": event_type, **data})

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
        # Clear old events
        if len(self.events) > 100: self.events = self.events[-100:]
        
        for agent_id, state in self.agents.items():
            zone = self.get_zone(state.position)
            if zone == "park" and state.energy > 0:
                state.energy = min(100.0, state.energy + 3.0)
            
            if state.energy > 0:
                state.energy -= 0.5
                if state.energy <= 0:
                    state.energy = 0
                    logger.warning(f"Agent {agent_id} ({state.name}) has collapsed.")