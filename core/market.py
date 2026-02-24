from typing import List
from .models import Job, Position

class JobBoard:
    def __init__(self):
        self.available_jobs: List[Job] = []

    def post_job(self, job: Job):
        self.available_jobs.append(job)

    def take_job(self, agent_id: str) -> Job:
        if not self.available_jobs:
            return None
        # Simple FIFO for MVP
        return self.available_jobs.pop(0)

class Market:
    def __init__(self):
        self.job_board = JobBoard()
        self.resource_prices = {"food": 10.0, "materials": 25.0}