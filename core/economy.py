import uuid
from typing import List, Dict, Any
from datetime import datetime
from core.models import Transaction

class TransactionLedger:
    def __init__(self):
        self.history: List[Transaction] = []

    def record(self, sender: str, receiver: str, amount: float, purpose: str):
        tx = Transaction(
            id=str(uuid.uuid4()),
            sender_id=sender,
            receiver_id=receiver,
            amount=amount,
            purpose=purpose,
            timestamp=datetime.now().isoformat()
        )
        self.history.append(tx)
        return tx

class EconomySystem:
    def __init__(self):
        self.ledger = TransactionLedger()
        self.registry: Dict[str, List[str]] = {} # service_name -> [agent_ids]

    def register_service(self, agent_id: str, service_name: str):
        if service_name not in self.registry:
            self.registry[service_name] = []
        if agent_id not in self.registry[service_name]:
            self.registry[service_name].append(agent_id)

    def get_providers(self, service_name: str) -> List[str]:
        return self.registry.get(service_name, [])