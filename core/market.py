from typing import List, Dict
from .models import Job, Position, ResourceType

class JobBoard:
    def __init__(self):
        self.available_jobs: List[Job] = []

    def post_job(self, job: Job):
        self.available_jobs.append(job)

    def take_job(self, agent_id: str) -> Job:
        if not self.available_jobs:
            return None
        return self.available_jobs.pop(0)

class Market:
    def __init__(self):
        self.job_board = JobBoard()
        self.resource_prices: Dict[ResourceType, float] = {
            ResourceType.FOOD: 10.0, 
            ResourceType.MATERIALS: 25.0
        }