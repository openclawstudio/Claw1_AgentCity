import random
from core.models import ZoneType, Position

class Brain:
    def __init__(self):
        self.memory = []
        self.current_intention = None

    def decide_action(self, state, world):
        # Logic to clear intention if satisfied
        if self.current_intention == "rest" and state.energy > 90:
            self.current_intention = None
        elif self.current_intention == "work" and state.wallet.balance > 50:
            self.current_intention = None
        elif self.current_intention == "socialize" and state.happiness > 90:
            self.current_intention = None

        # Priority selection
        if state.energy < 30:
            self.current_intention = "rest"
        elif state.wallet.balance < 10:
            self.current_intention = "work"
        elif not self.current_intention:
            self.current_intention = random.choice(["socialize", "work", "rest"])
            
        return self.current_intention

    def get_target_position(self, action, current_pos, world):
        action_map = {
            "rest": ZoneType.RESIDENTIAL,
            "work": ZoneType.INDUSTRIAL,
            "socialize": ZoneType.COMMERCIAL
        }
        target_zone = action_map.get(action, ZoneType.RESIDENTIAL)
        return world.get_nearest_zone(current_pos, target_zone)