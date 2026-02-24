import random
import math
from .models import AgentState, ZoneType

class Agent:
    def __init__(self, agent_id: str, start_pos: tuple, job_role: str = "citizen"):
        self.id = agent_id
        self.state = AgentState(id=agent_id, pos=start_pos, job_role=job_role)
        self.alive = True

    def _move_towards(self, target_pos: tuple):
        tx, ty = target_pos
        x, y = self.state.pos
        dx = 1 if tx > x else -1 if tx < x else 0
        dy = 1 if ty > y else -1 if ty < y else 0
        return (x + dx, y + dy)

    def step(self, world):
        if not self.alive:
            return

        # 1. Decision Logic (Goal-based Movement)
        target_pos = None
        if self.state.energy < 30:
            # Seek residential zone to rest
            res_zones = world.get_zones_by_type(ZoneType.RESIDENTIAL)
            if res_zones:
                target_pos = min(res_zones, key=lambda p: math.dist(p, self.state.pos))
        elif self.state.wallet < 20:
            # Seek commercial zone to earn money
            com_zones = world.get_zones_by_type(ZoneType.COMMERCIAL)
            if com_zones:
                target_pos = min(com_zones, key=lambda p: math.dist(p, self.state.pos))

        if target_pos and target_pos != self.state.pos:
            new_pos = self._move_towards(target_pos)
        else:
            # Random walk if no specific goal
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
            new_pos = (max(0, min(world.width - 1, self.state.pos[0] + dx)),
                       max(0, min(world.height - 1, self.state.pos[1] + dy)))
        
        self.state.pos = new_pos
        
        # 2. Energy Consumption
        self.state.energy -= 0.5
        if self.state.energy <= 0:
            self.alive = False
            return
        
        # 3. Zone-based Actions
        current_zone = world.get_zone(self.state.pos)
        
        if current_zone == ZoneType.INDUSTRIAL:
            if self.state.energy > 40:
                self.state.inventory["resource"] = self.state.inventory.get("resource", 0) + 1
                self.state.energy -= 5.0
                # Post to market if they have surplus
                if self.state.inventory["resource"] >= 1:
                    world.market.post_offer(self.id, "resource", 15.0, 1)

        elif current_zone == ZoneType.COMMERCIAL:
            self.state.wallet += 5.0
            self.state.energy -= 2.0

        elif current_zone == ZoneType.RESIDENTIAL:
            if self.state.energy < 100:
                self.state.energy = min(100.0, self.state.energy + 10.0)

        # 4. Market Interaction (Buy food/resource if low energy)
        if self.state.energy < 40 and self.state.wallet >= 15:
            resource_offers = [oid for oid, o in world.market.offers.items() if o.item == "resource"]
            if resource_offers:
                if world.market.fulfill_offer(resource_offers[0], self, world.agent_map, world.tick_count, world.economy):
                    if self.state.inventory.get("resource", 0) > 0:
                        self.state.inventory["resource"] -= 1
                        self.state.energy = min(100.0, self.state.energy + 40.0)