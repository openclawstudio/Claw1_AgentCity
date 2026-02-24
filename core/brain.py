import random
from core.models import ZoneType, Position

class Brain:
    def __init__(self):
        self.memory = []

    def decide_action(self, state, world):
        # Simple heuristic decision making
        if state.energy < 30:
            return "seek_rest" # Residential
        elif state.wallet.balance < 10:
            return "seek_work" # Industrial
        else:
            return "socialize" # Commercial

    def get_target_position(self, action, current_pos, world):
        target_zone = ZoneType.RESIDENTIAL
        if action == "seek_work":
            target_zone = ZoneType.INDUSTRIAL
        elif action == "socialize":
            target_zone = ZoneType.COMMERCIAL

        # Find nearest zone of type
        best_pos = current_pos
        min_dist = float('inf')
        
        for coord, zone in world.grid.items():
            if zone == target_zone:
                dist = abs(coord[0] - current_pos.x) + abs(coord[1] - current_pos.y)
                if dist < min_dist:
                    min_dist = dist
                    best_pos = Position(x=coord[0], y=coord[1])
        
        return best_pos