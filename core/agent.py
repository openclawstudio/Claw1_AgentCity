import uuid
import random
import math
from typing import Optional
from .models import AgentState, Position, Job, InventoryItem, ResourceType, ZoneType
from .market import Market
from .economy import EconomyManager

class Citizen:
    """Represents an autonomous AI agent within the City simulation."""
    def __init__(self, name: str, pos: Position):
        self.state = AgentState(
            id=str(uuid.uuid4()),
            name=name,
            pos=pos
        )

    @property
    def id(self): return self.state.id
    
    @property
    def balance(self): return self.state.balance

    @balance.setter
    def balance(self, val): self.state.balance = val

    def step(self, market: Market, economy: EconomyManager, world):
        """Performs one simulation tick for the agent."""
        current_cell = world.get_cell(self.state.pos)
        
        # 1. Survival Logic: Buy food if energy is low and funds exist
        food_price = market.resource_prices.get(ResourceType.FOOD, 10.0)
        if self.state.energy < 30 and self.state.balance >= food_price:
            if current_cell.zone == ZoneType.COMMERCIAL:
                self.buy_resource(ResourceType.FOOD, market)
            else:
                self.move_towards_zone(ZoneType.COMMERCIAL, world)
            return
            
        # 2. Activity Logic
        if self.state.energy < 20:
            self.state.current_goal = "RESTING"
            self.state.energy = min(100.0, self.state.energy + 15.0)
        elif self.state.balance < 20:
            self.state.current_goal = "SEEKING_WORK"
            job = market.job_board.take_job(self.id)
            if job:
                if self.state.energy > job.energy_cost + 5:
                    self.work(job, economy, world)
                else:
                    market.job_board.post_job(job)
                    self.state.current_goal = "TOO_TIRED_FOR_WORK"
            else:
                self.move_randomly(world)
        else:
            self.state.current_goal = "WANDERING"
            self.move_randomly(world)
            self.state.energy -= 2

    def move_towards_zone(self, zone_type: ZoneType, world):
        """Calculates distance to nearest cell of zone_type and moves one step towards it."""
        best_dist = float('inf')
        target_pos = None

        for x in range(world.width):
            for y in range(world.height):
                if world.grid[x][y].zone == zone_type:
                    dist = math.sqrt((x - self.state.pos.x)**2 + (y - self.state.pos.y)**2)
                    if dist < best_dist:
                        best_dist = dist
                        target_pos = Position(x=x, y=y)
        
        if target_pos:
            dx = 1 if target_pos.x > self.state.pos.x else -1 if target_pos.x < self.state.pos.x else 0
            dy = 1 if target_pos.y > self.state.pos.y else -1 if target_pos.y < self.state.pos.y else 0
            self.move_to(Position(x=self.state.pos.x + dx, y=self.state.pos.y + dy), world)

    def move_to(self, new_pos: Position, world):
        """Safely updates agent position within the world grid boundaries."""
        new_pos.x = max(0, min(world.width - 1, new_pos.x))
        new_pos.y = max(0, min(world.height - 1, new_pos.y))
        
        # De-register from old cell
        old_cell = world.get_cell(self.state.pos)
        if self.id in old_cell.agents:
            old_cell.agents.remove(self.id)

        # Update state and register to new cell
        self.state.pos = new_pos
        world.get_cell(self.state.pos).agents.append(self.id)

    def move_randomly(self, world):
        moves = [(0,1), (0,-1), (1,0), (-1,0)]
        dx, dy = random.choice(moves)
        self.move_to(Position(x=self.state.pos.x + dx, y=self.state.pos.y + dy), world)

    def buy_resource(self, res_type: ResourceType, market: Market):
        cost = market.resource_prices.get(res_type, 100.0)
        if self.state.balance >= cost:
            self.state.balance -= cost
            if res_type == ResourceType.FOOD:
                self.state.energy = min(100.0, self.state.energy + 40.0)
            
            for item in self.state.inventory:
                if item.type == res_type:
                    item.amount += 1
                    return
            self.state.inventory.append(InventoryItem(type=res_type, amount=1.0))

    def work(self, job: Job, economy: EconomyManager, world):
        """Executes work logic: moves to site, costs energy, awards credits."""
        if self.state.energy < job.energy_cost:
            return
        self.move_to(job.location, world)
        self.state.energy -= job.energy_cost
        self.state.balance += job.payout
        economy.record_payout(job.employer_id, self.id, job.payout, job.title)
        job.completed = True