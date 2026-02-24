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
    def id(self): return self.state.id
    
    @property
    def balance(self): return self.state.balance
    @balance.setter
    def balance(self, val): self.state.balance = val

    def step(self, market: Market, economy: EconomyManager, world):
        # 1. Survival Logic: If low energy and has money, buy food
        if self.state.energy < 30 and self.state.balance >= market.resource_prices.get("food", 100):
            self.buy_resource("food", market)
            
        # 2. Activity Logic
        if self.state.energy < 20:
            self.state.current_goal = "RESTING"
            self.state.energy = min(100.0, self.state.energy + 10.0)
        elif self.state.balance < 20:
            self.state.current_goal = "SEEKING_WORK"
            job = market.job_board.take_job(self.id)
            if job:
                self.work(job, economy)
            else:
                self.move_randomly(world)
        else:
            self.state.current_goal = "WANDERING"
            self.move_randomly(world)
            self.state.energy -= 2

    def move_randomly(self, world):
        # Remove from old cell
        world.get_cell(self.state.pos).agents.remove(self.id)
        
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)
        
        # Add to new cell
        world.get_cell(self.state.pos).agents.append(self.id)

    def buy_resource(self, resource_name: str, market: Market):
        cost = market.resource_prices.get(resource_name, 100)
        if self.state.balance >= cost:
            self.state.balance -= cost
            if resource_name == "food":
                self.state.energy = min(100.0, self.state.energy + 40.0)
            
            # Update Inventory
            found = False
            for item in self.state.inventory:
                if item.type.value == resource_name:
                    item.amount += 1
                    found = True
                    break
            if not found:
                self.state.inventory.append(InventoryItem(type=ResourceType.FOOD if resource_name == "food" else ResourceType.MATERIALS, amount=1))
                
            print(f"Agent {self.state.name} bought {resource_name} for {cost}")

    def work(self, job: Job, economy: EconomyManager):
        # Update world position
        self.state.pos = job.location
        self.state.energy -= job.energy_cost
        
        # Financial transaction
        economy.ledger.record(job.employer_id, self.id, job.payout, f"Job: {job.title}")
        self.state.balance += job.payout
        economy.global_gdp += job.payout
        job.completed = True
        print(f"Agent {self.state.name} completed job: {job.title} (+{job.payout})")