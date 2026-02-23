import random
from core.models import AgentState, Vector2D, JobStatus

class CitizenAgent:
    def __init__(self, state: AgentState):
        self.state = state

    def decide_action(self, world):
        """Basic AI logic for the MVP"""
        if self.state.energy < 30:
            self.move_towards(Vector2D(x=5, y=5)) # Head to Park
        elif self.state.economy.balance < 10:
            self.look_for_work(world)
        else:
            self.wander()

    def move_towards(self, target: Vector2D):
        if self.state.position.x < target.x: self.state.position.x += 1
        elif self.state.position.x > target.x: self.state.position.x -= 1
        if self.state.position.y < target.y: self.state.position.y += 1
        elif self.state.position.y > target.y: self.state.position.y -= 1

    def wander(self):
        self.state.position.x = max(0, min(49, self.state.position.x + random.choice([-1, 0, 1])))
        self.state.position.y = max(0, min(49, self.state.position.y + random.choice([-1, 0, 1])))

    def look_for_work(self, world):
        # Simple labor mechanic for MVP
        zone = world.get_zone(self.state.position)
        if zone == "market":
            self.state.economy.balance += 5
            self.state.energy -= 5