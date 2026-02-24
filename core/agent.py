import random
from .models import AgentState, ZoneType

class Agent:
    def __init__(self, agent_id: str, start_pos: tuple, job_role: str = "citizen"):
        self.id = agent_id
        self.state = AgentState(id=agent_id, pos=start_pos, job_role=job_role)

    def step(self, world):
        # 1. Movement Logic
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        new_x = max(0, min(world.width - 1, self.state.pos[0] + dx))
        new_y = max(0, min(world.height - 1, self.state.pos[1] + dy))
        self.state.pos = (new_x, new_y)
        
        # 2. Energy Consumption
        self.state.energy -= 0.5
        
        # 3. Zone-based Actions
        current_zone = world.get_zone(self.state.pos)
        
        if current_zone == ZoneType.INDUSTRIAL:
            # Production logic: Produce goods if they have energy
            if self.state.energy > 20:
                self.state.inventory["resource"] = self.state.inventory.get("resource", 0) + 1
                self.state.energy -= 2.0
                # Post to market if they have surplus
                if self.state.inventory["resource"] > 5:
                    world.market.post_offer(self.id, "resource", 10.0, 1)

        elif current_zone == ZoneType.COMMERCIAL:
            # Work/Trade logic
            self.state.wallet += 2.0
            self.state.energy -= 1.0
            # Record interaction in economy ledger (simulated transaction from 'City Bank')
            # Note: In a full system, this would be a transaction from a business agent

        elif current_zone == ZoneType.RESIDENTIAL:
            # Recover energy
            if self.state.energy < 80:
                self.state.energy += 5.0

        # 4. Survival: If energy is low, try to buy resources if available
        if self.state.energy < 20 and self.state.wallet >= 10:
            resource_offers = [oid for oid, o in world.market.offers.items() if o.item == "resource"]
            if resource_offers:
                if world.market.fulfill_offer(resource_offers[0], self, world.agents):
                    self.state.energy += 20.0 # Consume item immediately