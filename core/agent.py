import uuid
from .models import AgentState, Position, Job

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

    def step(self, market, economy, world):
        # Basic Logic Loop
        if self.state.energy < 30:
            self.state.current_goal = "RECOVERY"
            self.state.energy += 10
        elif self.state.balance < 20:
            job = market.job_board.take_job(self.id)
            if job:
                self.work(job, economy)
        else:
            self.move_randomly(world)
            self.state.energy -= 2

    def move_randomly(self, world):
        dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = max(0, min(world.width - 1, self.state.pos.x + dx))
        new_y = max(0, min(world.height - 1, self.state.pos.y + dy))
        self.state.pos = Position(x=new_x, y=new_y)

    def work(self, job: Job, economy):
        self.state.pos = job.location
        self.state.energy -= job.energy_cost
        self.state.balance += job.payout
        print(f"Agent {self.state.name} completed job: {job.title}")

import random