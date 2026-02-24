import random
from core.models import AgentState, ResourceType, Position

class CitizenAgent:
    def __init__(self, agent_id: str, name: str, x: int, y: int):
        self.state = AgentState(
            id=agent_id,
            name=name,
            position=Position(x=x, y=y),
            inventory={ResourceType.CREDITS: 100.0, ResourceType.ENERGY: 50.0}
        )

    def step(self, world):
        # Consume energy
        self.state.energy_level -= 1.0
        
        # Simple Logic: Move if energy high, stay if low
        if self.state.energy_level > 20:
            self.state.position.x = max(0, min(world.width - 1, self.state.position.x + random.randint(-1, 1)))
            self.state.position.y = max(0, min(world.height - 1, self.state.position.y + random.randint(-1, 1)))
            self.state.status = "exploring"
        else:
            self.state.status = "resting"
            self.recharge()

    def recharge(self):
        if self.state.inventory.get(ResourceType.CREDITS, 0) >= 5:
            self.state.inventory[ResourceType.CREDITS] -= 5
            self.state.energy_level += 20
            print(f"Agent {self.state.name} recharged.")
