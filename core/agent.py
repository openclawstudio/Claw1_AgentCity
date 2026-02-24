import uuid
import random
from .models import AgentState, Position, Job
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
        if self.state.energy < 30 and self.state.balance >= market.resource_prices["food"]:
            self.buy_resource("food", market)
            
        # 2. Activity Logic
        if self.state.energy < 20:
            self.state.current_goal = "RESTING"
            self.state.energy += 5
        elif self.state.balance < 20:
            self.state.current_goal = "SEEKING_WORK"
            job = market.job_board.take_job(self.id)
            if job:
                self.work(job, economy)
        else:
            self.state.current_goal = "WANDERING"
            self.move_randomly(world)
            self.state.energy -= 2

    def move_randomly(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)

    def buy_resource(self, resource_type: str, market: Market):
        cost = market.resource_prices.get(resource_type, 100)
        if self.state.balance >= cost:
            self.state.balance -= cost
            if resource_type == "food":
                self.state.energy += 40
            print(f"Agent {self.state.name} bought {resource_type} for {cost}")

    def work(self, job: Job, economy: EconomyManager):
        self.state.pos = job.location
        self.state.energy -= job.energy_cost
        # Use economy manager to track the transaction
        # In this MVP, SYSTEM acts as the central bank for jobs
        economy.ledger.record("SYSTEM", self.id, job.payout, f"Job: {job.title}")
        self.state.balance += job.payout
        economy.global_gdp += job.payout
        print(f"Agent {self.state.name} completed job: {job.title} (+{job.payout})")
