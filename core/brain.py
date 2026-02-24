import random
from core.models import ZoneType, Position

class Brain:
    def __init__(self):
        self.memory = []
        self.current_intention = None

    def decide_action(self, state, world):
        # Prioritize survival: Energy > Wealth > Social
        if state.energy < 25:
            self.current_intention = "rest"
        elif state.wallet.balance < 5:
            self.current_intention = "work"
        elif state.energy > 60 and state.wallet.balance > 20:
            self.current_intention = "socialize"
        elif not self.current_intention:
            self.current_intention = "socialize"
            
        return self.current_intention

    def get_target_position(self, action, current_pos, world):
        action_map = {
            "rest": ZoneType.RESIDENTIAL,
            "work": ZoneType.INDUSTRIAL,
            "socialize": ZoneType.COMMERCIAL
        }
        target_zone = action_map.get(action, ZoneType.RESIDENTIAL)
        
        # Delegate spatial lookup to world layer (optimized cache)
        return world.get_nearest_zone(current_pos, target_zone)