import uuid
import random
from typing import Optional
from .models import AgentState, Position, Job, InventoryItem, ResourceType
from .market import Market
from .economy import EconomyManager

class Citizen:
    def __init__(self, name: str, pos: Position):
        self.state = AgentState(
            id=str(uuid.uuid4()),
            name=name,
            pos=pos
        )

    @property
    def id(self):
        return self.state.id
    
    @property
    def balance(self):
        return self.state.balance

    @balance.setter
    def balance(self, val):
        self.state.balance = val

    def step(self, market: Market, economy: EconomyManager, world):
        # 1. Survival Logic: If low energy and has money, buy food
        food_price = market.resource_prices.get(ResourceType.FOOD, 10.0)
        if self.state.energy < 30 and self.state.balance >= food_price:
            self.buy_resource(ResourceType.FOOD, market)
            
        # 2. Activity Logic
        if self.state.energy < 20:
            self.state.current_goal = "RESTING"
            self.state.energy = min(100.0, self.state.energy + 15.0)
        elif self.state.balance < 20:
            self.state.current_goal = "SEEKING_WORK"
            job = market.job_board.take_job(self.id)
            if job:
                self.work(job, economy, world)
            else:
                self.move_randomly(world)
        else:
            self.state.current_goal = "WANDERING"
            self.move_randomly(world)
            self.state.energy -= 2

    def move_randomly(self, world):
        # Safe removal from current location
        current_cell = world.get_cell(self.state.pos)
        if self.id in current_cell.agents:
            current_cell.agents.remove(self.id)
        
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)
        
        # Add to new cell tracking
        world.get_cell(self.state.pos).agents.append(self.id)

    def buy_resource(self, res_type: ResourceType, market: Market):
        cost = market.resource_prices.get(res_type, 100.0)
        if self.state.balance >= cost:
            self.state.balance -= cost
            if res_type == ResourceType.FOOD:
                self.state.energy = min(100.0, self.state.energy + 40.0)
            
            # Update Inventory
            found = False
            for item in self.state.inventory:
                if item.type == res_type:
                    item.amount += 1
                    found = True
                    break
            if not found:
                self.state.inventory.append(InventoryItem(type=res_type, amount=1.0))
                
            print(f"Agent {self.state.name} bought {res_type.value} for {cost}")

    def work(self, job: Job, economy: EconomyManager, world):
        # Ensure agent is moved to the job site
        old_cell = world.get_cell(self.state.pos)
        if self.id in old_cell.agents:
            old_cell.agents.remove(self.id)
            
        self.state.pos = job.location
        world.get_cell(self.state.pos).agents.append(self.id)
        
        # Process work mechanics
        self.state.energy -= job.energy_cost
        self.state.balance += job.payout
        
        # Financial transaction record through central manager
        economy.record_payout(job.employer_id, self.id, job.payout, job.title)
        
        job.completed = True
        print(f"Agent {self.state.name} completed job: {job.title} (+{job.payout})")