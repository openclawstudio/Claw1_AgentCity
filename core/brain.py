import random
from core.models import ZoneType, Position

class Brain:
    def __init__(self):
        self.memory = []
        self._cached_targets = {}

    def decide_action(self, state, world):
        # Simple heuristic decision making based on needs
        if state.energy < 30:
            return "rest"
        elif state.wallet.balance < 10:
            return "work"
        else:
            return "socialize"

    def get_target_position(self, action, current_pos, world):
        # Map actions to ZoneTypes
        action_map = {
            "rest": ZoneType.RESIDENTIAL,
            "work": ZoneType.INDUSTRIAL,
            "socialize": ZoneType.COMMERCIAL
        }
        target_zone = action_map.get(action, ZoneType.RESIDENTIAL)

        # Use cached target if valid, otherwise find nearest
        best_pos = current_pos
        min_dist = float('inf')
        found = False
        
        # Simple spatial lookup optimization: check world grid
        for coord, zone in world.grid.items():
            if zone == target_zone:
                dist = abs(coord[0] - current_pos.x) + abs(coord[1] - current_pos.y)
                if dist < min_dist:
                    min_dist = dist
                    best_pos = Position(x=coord[0], y=coord[1])
                    found = True
                    if dist == 0: break # Already there
        
        return best_pos if found else current_pos