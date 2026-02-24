import random
import math
from .models import AgentState, ZoneType

class Agent:
    def __init__(self, agent_id: str, start_pos: tuple, job_role: str = "citizen"):
        self.id = agent_id
        self.state = AgentState(id=agent_id, pos=start_pos, job_role=job_role)
        self.alive = True
        self.workplace: tuple = None

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
        
        # Assign workplace if none exists and agent has a role
        if not self.workplace and self.state.job_role != "citizen":
            possible_sites = []
            if self.state.job_role in ["worker", "producer"]:
                possible_sites = world.get_zones_by_type(ZoneType.INDUSTRIAL)
            elif self.state.job_role in ["merchant", "builder"]:
                possible_sites = world.get_zones_by_type(ZoneType.COMMERCIAL)
            
            if possible_sites:
                self.workplace = random.choice(possible_sites)

        # Determine destination priority
        if self.state.energy < 30:
            res_zones = world.get_zones_by_type(ZoneType.RESIDENTIAL)
            if res_zones:
                target_pos = min(res_zones, key=lambda p: math.dist(p, self.state.pos))
        elif self.state.wallet < 20 or (self.workplace and self.state.energy > 50):
            target_pos = self.workplace

        if target_pos and target_pos != self.state.pos:
            new_pos = self._move_towards(target_pos)
        else:
            # Wander or stay put
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
            new_pos = (max(0, min(world.width - 1, self.state.pos[0] + dx)),
                       max(0, min(world.height - 1, self.state.pos[1] + dy)))
        
        self.state.pos = new_pos
        
        # 2. Energy Consumption
        # Base metabolism cost
        self.state.energy -= 0.5
        if self.state.energy <= 0:
            self.alive = False
            return
        
        # 3. Zone-based Actions
        current_zone = world.get_zone(self.state.pos)
        
        if current_zone == ZoneType.INDUSTRIAL:
            # Production logic for industrial workers
            if self.state.job_role in ["producer", "worker"] and self.state.energy > 40.0:
                self.state.inventory["resource"] = self.state.inventory.get("resource", 0) + 1
                self.state.energy -= 10.0
                
                # Create offer only if we have stock not already listed
                listed_qty = sum(o.quantity for o in world.market.offers.values() if o.creator_id == self.id)
                actual_qty = self.state.inventory.get("resource", 0)
                if actual_qty > listed_qty:
                    world.market.post_offer(self.id, "resource", 12.0, 1, self.state.inventory)

        elif current_zone == ZoneType.COMMERCIAL:
            # Economic participation: Working for wage
            if self.state.energy > 20.0:
                self.state.wallet += 10.0
                self.state.energy -= 5.0

        elif current_zone == ZoneType.RESIDENTIAL:
            # Rest logic with cost
            if self.state.energy < 100 and self.state.wallet >= 2.0:
                self.state.energy = min(100.0, self.state.energy + 25.0)
                self.state.wallet -= 2.0

        # 4. Market Interaction (Consumption)
        # If hungry/low energy, try to buy and consume a resource
        if self.state.energy < 50 and self.state.wallet >= 15:
            resource_offers = [oid for oid, o in world.market.offers.items() if o.item == "resource" and o.creator_id != self.id]
            if resource_offers:
                # Sort by price (Greedy buyer)
                resource_offers.sort(key=lambda oid: world.market.offers[oid].price)
                if world.market.fulfill_offer(resource_offers[0], self, world.agent_map, world.tick_count, world.economy):
                    if self.state.inventory.get("resource", 0) > 0:
                        self.state.inventory["resource"] -= 1
                        self.state.energy = min(100.0, self.state.energy + 40.0)
