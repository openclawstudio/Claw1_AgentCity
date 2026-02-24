import uuid
from core.models import Position, AgentState, Transaction, ZoneType
from core.brain import Brain

class Citizen:
    ENERGY_DECAY = 0.4
    WORK_REWARD = 12.0
    WORK_COST = 10.0
    REST_RECOVERY = 30.0
    SOCIAL_COST = 4.0
    SOCIAL_REWARD = 15.0

    def __init__(self, name: str, x: int, y: int):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.pos = Position(x=x, y=y)
        self.state = AgentState()
        self.brain = Brain()

    def step(self, world):
        # 1. Decide action
        action = self.brain.decide_action(self.state, world)
        self.state.status_message = f"Intending to {action}"
        
        # 2. Identify target
        target = self.brain.get_target_position(action, self.pos, world)
        
        # 3. Move or Act
        if self.pos != target:
            self._move_towards(target)
        else:
            current_zone = world.get_zone(self.pos)
            self._process_zone_effects(current_zone, world)
        
        # 4. State Decay
        self.state.energy = max(0.0, self.state.energy - self.ENERGY_DECAY)
        if self.state.energy <= 0:
            self.state.happiness = max(0.0, self.state.happiness - 1.0)
            self.state.status_message = "Starving/Exhausted"

    def _move_towards(self, target: Position):
        new_x, new_y = self.pos.x, self.pos.y
        if self.pos.x != target.x:
            new_x += 1 if target.x > self.pos.x else -1
        if self.pos.y != target.y:
            new_y += 1 if target.y > self.pos.y else -1
        
        self.pos = Position(x=new_x, y=new_y)

    def _process_zone_effects(self, zone, world):
        if zone == ZoneType.INDUSTRIAL:
            self.state.wallet.balance += self.WORK_REWARD
            self.state.energy = max(0.0, self.state.energy - self.WORK_COST)
            self.state.status_message = "Working"
            world.record_transaction(Transaction(
                sender_id="SYSTEM_TREASURY",
                receiver_id=self.id,
                amount=self.WORK_REWARD,
                service_type="labor",
                timestamp=world.tick_counter
            ))
        elif zone == ZoneType.RESIDENTIAL:
            self.state.energy = min(100.0, self.state.energy + self.REST_RECOVERY)
            self.state.status_message = "Resting"
        elif zone == ZoneType.COMMERCIAL:
            if self.state.wallet.balance >= self.SOCIAL_COST:
                self.state.wallet.balance -= self.SOCIAL_COST
                self.state.happiness = min(100.0, self.state.happiness + self.SOCIAL_REWARD)
                self.state.status_message = "Socializing"
                world.record_transaction(Transaction(
                    sender_id=self.id,
                    receiver_id="COMMERCIAL_VENDORS",
                    amount=self.SOCIAL_COST,
                    service_type="consumption",
                    timestamp=world.tick_counter
                ))
            else:
                self.state.status_message = "Broke at Mall"