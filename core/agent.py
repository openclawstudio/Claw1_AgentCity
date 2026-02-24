import uuid
from core.models import Position, AgentState, Transaction
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

    def _move_towards(self, target):
        if self.pos.x < target.x: self.pos.x += 1
        elif self.pos.x > target.x: self.pos.x -= 1
        if self.pos.y < target.y: self.pos.y += 1
        elif self.pos.y > target.y: self.pos.y -= 1

    def _process_zone_effects(self, zone, world):
        from core.models import ZoneType
        if zone == ZoneType.INDUSTRIAL:
            self.state.wallet.balance += 2.0
            self.state.energy -= 1.0
        elif zone == ZoneType.RESIDENTIAL:
            self.state.energy = min(100, self.state.energy + 5.0)
        elif zone == ZoneType.COMMERCIAL:
            if self.state.wallet.balance >= 1.0:
                self.state.wallet.balance -= 1.0
                self.state.happiness += 2.0