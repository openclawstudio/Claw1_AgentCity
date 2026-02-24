import uuid
from core.models import Position, AgentState, Transaction, ZoneType
from core.brain import Brain

class Citizen:
    def __init__(self, name: str, x: int, y: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.pos = Position(x=x, y=y)
        self.state = AgentState()
        self.brain = Brain()

    def step(self, world):
        # 1. Decide
        action = self.brain.decide_action(self.state, world)
        
        # 2. Plan path
        target = self.brain.get_target_position(action, self.pos, world)
        
        # 3. Move
        self._move_towards(target)

        # 4. Perform Action / Economic loop
        current_zone = world.get_zone(self.pos)
        self._process_zone_effects(current_zone, world)
        
        # 5. Decay
        self.state.energy -= 0.5
        self.state.energy = max(0, self.state.energy)

    def _move_towards(self, target):
        if self.pos.x < target.x: self.pos.x += 1
        elif self.pos.x > target.x: self.pos.x -= 1
        if self.pos.y < target.y: self.pos.y += 1
        elif self.pos.y > target.y: self.pos.y -= 1

    def _process_zone_effects(self, zone, world):
        if zone == ZoneType.INDUSTRIAL:
            # Work logic: Earn money at cost of energy
            income = 2.0
            self.state.wallet.balance += income
            self.state.energy -= 1.0
            world.record_transaction(Transaction(
                sender_id="SYSTEM_TREASURY",
                receiver_id=self.id,
                amount=income,
                service_type="labor",
                timestamp=world.tick_counter
            ))
        elif zone == ZoneType.RESIDENTIAL:
            # Rest logic
            self.state.energy = min(100, self.state.energy + 5.0)
        elif zone == ZoneType.COMMERCIAL:
            # Consumption logic: Spend money for happiness
            if self.state.wallet.balance >= 1.0:
                cost = 1.0
                self.state.wallet.balance -= cost
                self.state.happiness = min(100, self.state.happiness + 2.0)
                world.record_transaction(Transaction(
                    sender_id=self.id,
                    receiver_id="COMMERCIAL_VENDORS",
                    amount=cost,
                    service_type="consumption",
                    timestamp=world.tick_counter
                ))